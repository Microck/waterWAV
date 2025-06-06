<div align="center">

<p>
	<a href="https://github.com/Microck/waterWAV">
		<img src="https://github.com/user-attachments/assets/f7bc0b37-05bd-4cc1-917d-88eb61287cfd" alt="waterWAV Banner"/>
	</a>
</p>
<p>
	<strong>Python script to embed visual watermarks directly into audio file spectrograms using STFT.</strong>
</p>

<p>
	<img src="https://img.shields.io/github/license/Microck/waterWAV?style=for-the-badge" alt="License"></a>
	<img src="https://img.shields.io/github/last-commit/Microck/waterWAV?style=for-the-badge" alt="Last Commit"></a>
</p>

</div>

## Overview

This tool allows you to take an image and embed it as a visual pattern within the spectrogram of an audio file. The process involves performing a Short-Time Fourier Transform (STFT) on the audio, preparing the image as a mask, and then attenuating specific frequency components in the audio corresponding to the dark areas of the image. This creates a "hidden" image in the audio's frequency representation, often visible when the audio is analyzed with a spectrogram viewer.

Inspired by artists like Aphex Twin and C418 who have famously embedded images in their tracks, and after seeing techniques discussed in videos like "an interesting way to watermark audio" by idiotinium, this script aims to make this fascinating process accessible to everyone. Taking a concept that might seem complex or niche and developing a tool that simplifies it empowers many more people to experiment and utilize the technique, whether for artistic expression, a bit of fun, or practical identification.

## Features

-   Embeds user-provided images into audio spectrograms.
-   Utilizes Short-Time Fourier Transform (STFT) for frequency domain manipulation.
-   Allows user to specify input audio and watermark image files.
-   Watermark is embedded within a defined frequency range (default: 200 Hz - 10700 Hz).
-   Adjustable attenuation factor to control the "visibility" or subtlety of the watermark.
-   Visualizes both the original and watermarked spectrograms for comparison.
-   User-friendly command-line interface with autodetection for common filenames.
-   Outputs a new audio file with the embedded watermark.

## Requirements

-   Python 3.x
-   Libraries: `numpy`, `librosa`, `matplotlib`, `Pillow`, `soundfile`

Install the required libraries using the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Usage

1.  **Prepare your files:**
    *   **Audio File:** Have your input audio file (e.g., `.wav`, `.mp3`).
    *   **Watermark Image:**
        *   Use a clear, high-contrast image (preferably **black and white**). Brighter areas of the image will form the watermark.
        *   The script resizes the image to fit the audio's duration and the specified frequency band. The original aspect ratio will likely be altered. Simple logos or symbols work best.
        *   Common formats like PNG or JPG are supported.

2.  **Run the script:**
    Execute the script by doble clicking it. 

3.  **Output:**
    *   A new audio file (default: `watermarked_audio.wav`) will be saved in the script's directory.
    *   A plot will display the original and watermarked spectrograms.

**Important Notes:**
*   The visibility of the watermark in the spectrogram and its audibility depend on the audio content, the chosen image, and the `attenuation_factor` (default is `0.05` for strong visibility; closer to `1.0` is more subtle). You can adjust this in the `watermark_audio` function within the `embedwatermark.py` script.
*   The image is flipped horizontally by the script to ensure correct orientation in the spectrogram.

## Example

This script can be used to add an artistic signature to an audio track, create an Easter egg for listeners, or simply experiment with audio-visual manipulation.
I personally use it as an easter egg in some of my keyboard sound tests. You can check it yourself by downloading the [video](https://youtu.be/YzaJVl_TQVw) and checking the audio's spectrogram.

![waterwavdemonstration](https://github.com/user-attachments/assets/e5def000-d5ea-4b0c-9433-ba43bc0571c4)


## Limitations

-   **Not for Security:** This method is for visual/artistic watermarking and is not a robust or secure method for copyright protection or anti-piracy. The watermark can be easily detected and potentially removed or altered with audio processing knowledge.
-   **Audibility:** Depending on the `attenuation_factor` and the audio content, the watermark might introduce audible artifacts. A lower attenuation factor (making the watermark darker/stronger) increases the chance of audibility.
-   **Image Distortion:** The watermark image is resized to fit the audio's duration and the fixed frequency band, which will change its aspect ratio.
-   **Fixed Frequency Band:** The default frequency range for embedding is 200 Hz to 10700 Hz. While this can be changed in the code (`prepare_watermark` function in `embedwatermark.py`), it's not a runtime option.
-   **Content Dependent:** The effectiveness and visibility can vary greatly depending on the spectral content of the original audio.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
