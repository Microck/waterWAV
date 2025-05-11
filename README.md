
![waterwav](https://github.com/user-attachments/assets/70fad97b-c4f4-4f19-8c9c-3c1745ce8dc4)

# waterWAV

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

After getting the video "an interesting way to watermark audio" by idiotinium in my recommended feed a few months ago, I decided to work on an easy way to hide watermarks in audio, accesible to everyone and anyone. Taking a concept that might seem complex or niche and developing a tool that simplifies it empowers many more people to experiment and utilize the technique, whether for artistic expression, a bit of fun, or practical identification.

![Screenshot_1140](https://github.com/user-attachments/assets/eeb0bc42-a95b-4ab6-b131-ea70fc462284)

---

## How to Use

This script allows you to embed a visual watermark (an image) into the spectrogram of an audio file.

**1. Prerequisites:**

*   **Python 3.x:** Ensure you have Python 3 installed.
*   **Dependencies:** Install the required Python libraries. Navigate to the script's directory in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```

**2. Prepare Your Files:**

*   **Audio File:**
    *   Have your input audio file ready (e.g., `.wav`, `.mp3`). Common formats supported by Librosa should work.
    *   You can place it in the same directory as the script and name it `input_audio.wav` for autodetection, or you'll be prompted for its path.
*   **Watermark Image:**
    *   **Format:** Use a common image format like PNG or JPG.
    *   **Content & Color:** For best and most predictable results, use a **clear, high-contrast, black and white image**.
        *   The script converts the image to grayscale.
        *   **Darker areas (pixels with values less than 128 on a 0-255 scale) will form the "visible" part of the watermark.** These areas will correspond to attenuated (quieter) frequencies in the audio's spectrogram.
        *   Lighter areas will have minimal to no effect on the audio.
    *   **Dimensions & Aspect Ratio:**
        *   The script will automatically resize your image.
        *   The **height** of the watermark in the spectrogram is determined by the hardcoded frequency range in the script (currently 200 Hz to 10700 Hz).
        *   The **width** of the watermark will be stretched or compressed to match the total duration (number of time frames) of your audio file.
        *   **Important:** Because of this resizing, the **original aspect ratio of your image will likely be altered** in the final spectrogram. Images that are very wide or very tall relative to the audio's duration might appear significantly distorted. Simple logos, symbols, or bold, short text tend to work better than highly detailed or complex images.
    *   You can place your watermark image in the same directory as the script and name it `watermark.png` for autodetection, or you'll be prompted for its path. The script handles the necessary orientation (it flips the image horizontally to appear correctly in the spectrogram).

**3. Run the Script:**

*   Execute the script using:
    ```bash
    python embedwatermark.py
    ```

**4. Output:**

*   **Watermarked Audio File:** A new audio file named `watermarked_audio.wav` will be saved in the same directory as the script. This file contains the embedded watermark.
*   **Spectrogram Visualization:** A Matplotlib window will pop up showing two spectrograms:
    *   The original audio's spectrogram.
    *   The watermarked audio's spectrogram, where you should be able to visually identify your watermark in the specified frequency range.

**5. Customization (Optional - Advanced):**

*   **Attenuation Factor:** You can adjust the `attenuation_factor` in the `embed_watermark` function call within the `watermark_audio` function.
    *   A value closer to `0.0` (e.g., `0.05`) makes the watermark more prominent (darker in the spectrogram, more audible change).
    *   A value closer to `1.0` (e.g., `0.5`) makes it more subtle.
*   **Frequency Range:** The embedding frequency range (`freq_start_hz` and `freq_end_hz`) is defined in the `prepare_watermark` function. You can modify these values if you need to target different frequency bands.

---

**Example Workflow:**

1.  Save your audio as `input_audio.wav` in the script's folder.
2.  Save your black and white logo as `watermark.png` in the script's folder.
3.  Run `pip install -r requirements.txt`.
4.  Run `python embedwatermark.py`.
5.  Check for `watermarked_audio.wav` and observe the displayed spectrograms.

