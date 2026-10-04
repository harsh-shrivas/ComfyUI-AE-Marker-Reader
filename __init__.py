import os
import tempfile
import subprocess
import time

class AEMarkerReaderNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trigger_signal": ("STRING", {"forceInput": True}),
            },
            "optional": {
                "marker_layer_name": ("STRING", {"default": "QA_Error_Markers"}),
                "report_file_path": ("STRING", {
                    "default": os.path.join(tempfile.gettempdir(), "ae_qa_report.txt"),
                    "multiline": False
                }),
                "ae_install_path": ("STRING", {
                    "default": r"C:\Program Files\Adobe\Adobe After Effects <VERSION>\Support Files\afterfx.exe",
                    "multiline": False
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("qa_report_text",)
    FUNCTION = "fetch_and_format_markers"
    OUTPUT_NODE = True
    CATEGORY = "Automation/AI Brain"

    @classmethod
    def IS_CHANGED(s, trigger_signal, **kwargs):
        return float(time.time())

    def fetch_and_format_markers(self, trigger_signal, marker_layer_name="QA_Error_Markers", report_file_path="", ae_install_path=""):
        if not report_file_path:
            report_file_path = os.path.join(tempfile.gettempdir(), "ae_qa_report.txt")
        clean_report_path = report_file_path.replace("\\", "/")

        # 100% Local ExtendScript execution - zero external API dependencies
        jsx_script = f'''
        (function() {{
            var comp = app.project.activeItem;
            if (!comp || !(comp instanceof CompItem)) return;

            var targetLayer = null;
            for (var i = 1; i <= comp.numLayers; i++) {{
                if (comp.layer(i).name === "{marker_layer_name}") {{
                    targetLayer = comp.layer(i);
                    break;
                }}
            }}

            if (!targetLayer) {{
                // Fallback to top layer if specific layer name not found
                targetLayer = comp.layer(1);
            }}
            if (!targetLayer) return;

            var markerProp = targetLayer.property("Marker");
            var numMarkers = markerProp.numKeys;
            var outText = "";

            for (var k = 1; k <= numMarkers; k++) {{
                var tVal = markerProp.keyTime(k);
                var comment = markerProp.keyValue(k).comment;

                var fps = comp.frameRate;
                var totalFrames = Math.floor(tVal * fps);
                var min = Math.floor(tVal / 60);
                var sec = Math.floor(tVal % 60);
                var frame = totalFrames % Math.round(fps);

                var pad = function(n) {{ return (n < 10 ? "0" : "") + n; }};
                var timeCode = pad(min) + "." + pad(sec) + "." + pad(frame);

                outText += "#" + k + " [" + timeCode + "]\\n";
                outText += comment + "\\n";
                outText += "------------------------------------------\\n";
            }}

            var outFile = new File("{clean_report_path}");
            outFile.open("w");
            outFile.write(outText);
            outFile.close();
        }})();
        '''

        temp_jsx = os.path.join(tempfile.gettempdir(), "read_ae_markers_local.jsx")
        with open(temp_jsx, "w", encoding="utf-8") as f:
            f.write(jsx_script)

        # Run script locally through After Effects CLI
        if os.path.exists(ae_install_path):
            try:
                subprocess.run([ae_install_path, "-r", temp_jsx], capture_output=True, text=True)
                time.sleep(0.5)
            except Exception as ex:
                print(f"[AE Marker Reader] Direct script execution failed: {ex}")

        # Read the resulting text file locally into ComfyUI
        if os.path.exists(clean_report_path):
            with open(clean_report_path, "r", encoding="utf-8") as f:
                report_content = f.read().strip()
            if report_content:
                return (report_content,)

        return ("No markers found on layer or AE project not open.",)


NODE_CLASS_MAPPINGS = {"AEMarkerReaderNode": AEMarkerReaderNode}
NODE_DISPLAY_NAME_MAPPINGS = {"AEMarkerReaderNode": "AE Marker Reader & Formatter"}