# ComfyUI-AE-Marker-Reader

A high-precision, automated bridge between Adobe After Effects and ComfyUI that extracts timeline markers, QA notes, and frame-accurate timecodes directly into ComfyUI via native ExtendScript CLI execution.

Built for VFX compositors, animators, and pipeline TDs who need automated quality control, review notes ingestion, and timeline-driven data synchronization with zero external dependencies and zero API costs.

---

## Features

* **Zero External Dependencies:** Runs entirely on native Python and After Effects' built-in ExtendScript engine (`afterfx.exe -r`) without extra pip packages.
* **100% Local Execution:** Executes locally on your workstation with zero LLM tokens or cloud dependencies.
* **Frame-Accurate Timecodes:** Automatically calculates and formats comp frame rates into standard `MM.SS.FF` timecodes alongside marker comments.
* **Targeted Layer Ingestion:** Reads markers from specific QA layers (e.g., `QA_Error_Markers`) with automatic fallback to the top layer.
* **Live Trigger Pipeline:** Accepts dynamic trigger signals to re-evaluate and fetch the latest timeline status on demand.

---

## Installation

1. Navigate to your ComfyUI custom nodes directory: `cd ComfyUI/custom_nodes`
2. Clone this repository: `git clone https://github.com/harsh-shrivas/ComfyUI-AE-Marker-Reader.git`
3. Restart ComfyUI. (Zero external packages required).

---

## Usage

* **Category:** `Automation/AI Brain`
* **Node Name:** `AE Marker Reader & Formatter`
* Connect an execution string or upstream trigger into `trigger_signal`.
* Set `marker_layer_name` to your target marker layer (defaults to `QA_Error_Markers`).
* Verify `ae_install_path` points to your local `afterfx.exe` executable (e.g., `C:\Program Files\Adobe\Adobe After Effects <VERSION>\Support Files\afterfx.exe`).
* Click **Queue Prompt** to execute the local script, extract timeline markers, and output the formatted report string into downstream text or review nodes.

---

## Inputs & Outputs

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **trigger_signal** | `STRING` (Input) | Signal that forces node evaluation on graph execution |
| **marker_layer_name** | `STRING` (Optional) | Name of the comp layer holding the markers (defaults to `QA_Error_Markers`) |
| **report_file_path** | `STRING` (Optional) | Custom output text file path (defaults to system temporary directory) |
| **ae_install_path** | `STRING` (Optional) | Absolute path to the `afterfx.exe` executable |
| **qa_report_text** | `STRING` (Output) | Formatted timecoded QA marker report |

---

## License

MIT License. Free to use, modify, and integrate into internal studio and personal pipelines.
