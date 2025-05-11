import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from PIL import Image
import soundfile as sf
import os

def load_and_stft(audio_path, n_fft=2048, hop_length=512):
    """
    Loads audio and calculates its Short-Time Fourier Transform (STFT).

    Args:
        audio_path (str): Path to the input audio file.
        n_fft (int): Window size for the FFT.
        hop_length (int): Number of samples between consecutive STFT frames.

    Returns:
        tuple: Original audio time series, sampling rate, STFT, magnitude, phase.
    """
    try:
        y, sr = librosa.load(audio_path, sr=None)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None, None, None, None, None
    stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    mag, phase = librosa.magphase(stft)
    return y, sr, stft, mag, phase

def prepare_watermark(image_path, stft_shape, sr):
    """
    Prepares the watermark image as a binary mask for embedding.

    Args:
        image_path (str): Path to the watermark image file.
        stft_shape (tuple): Shape of the STFT magnitude spectrogram.
        sr (int): Sampling rate of the audio.

    Returns:
        tuple: Watermark mask, start frequency index, end frequency index.
    """
    # Define the frequency range for embedding (200 Hz to 10700 Hz)
    freq_start_hz = 200
    freq_end_hz = 10700

    # Convert frequency range from Hz to STFT bin indices
    # sr / 2 is the Nyquist frequency, corresponding to stft_shape[0] bins
    freq_start = int(freq_start_hz / (sr / 2) * stft_shape[0])
    freq_end = int(freq_end_hz / (sr / 2) * stft_shape[0])

    try:
        img = Image.open(image_path).convert('L') # Convert to grayscale
    except FileNotFoundError:
        print(f"Error: Watermark image not found at {image_path}")
        return None, None, None
    except Exception as e:
        print(f"Error opening or processing watermark image: {e}")
        return None, None, None

    # Calculate the required height for the resized image
    watermark_height = freq_end - freq_start

    # Resize the image to match the dimensions of the target region in the spectrogram
    # The width matches the number of time frames (stft_shape[1])
    img_resized = img.resize((stft_shape[1], watermark_height))

    # Explicitly flip the image horizontally to correct orientation in the spectrogram
    img_resized = img_resized.transpose(Image.FLIP_LEFT_RIGHT)

    # Convert the resized image to a NumPy array
    img_array = np.array(img_resized)

    # Create a binary mask: 1 where image is dark (< 128), 0 otherwise
    # This is because we want to attenuate the signal where the watermark is "present" (dark)
    img_binary = (img_array < 128).astype(np.float32)

    # Create a mask the same size as the spectrogram, initially all 1s
    mask = np.ones(stft_shape)

    # Place the binary watermark data into the defined frequency range of the mask
    mask[freq_start:freq_end, :] = img_binary

    return mask, freq_start, freq_end

def embed_watermark(magnitude, watermark_mask, freq_start, freq_end, attenuation_factor=0.1):
    """
    Embeds the watermark into the magnitude spectrogram by reducing magnitude
    in the watermark areas.

    Args:
        magnitude (np.ndarray): The magnitude spectrogram.
        watermark_mask (np.ndarray): The binary watermark mask (1 for watermark areas).
        freq_start (int): Start frequency index for embedding.
        freq_end (int): End frequency index for embedding.
        attenuation_factor (float): Factor by which to reduce the magnitude
                                    in the watermark areas (0 to 1). Lower
                                    values mean more attenuation (darker watermark).

    Returns:
        np.ndarray: The modified magnitude spectrogram.
    """
    modified_mag = magnitude.copy()
    target_region = modified_mag[freq_start:freq_end, :]

    # Reduce the magnitude in areas where the watermark mask is 1
    # This makes the "watermark" areas quieter and thus darker in the spectrogram
    target_region[watermark_mask[freq_start:freq_end, :] > 0.5] *= attenuation_factor

    modified_mag[freq_start:freq_end, :] = target_region
    return modified_mag

def visualize_spectrograms(original_mag, modified_mag, sr, hop_length=512):
    """
    Visualizes the original and watermarked spectrograms.

    Args:
        original_mag (np.ndarray): The original magnitude spectrogram.
        modified_mag (np.ndarray): The modified magnitude spectrogram.
        sr (int): Sampling rate of the audio.
        hop_length (int): Hop length used for STFT.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    kwargs = dict(
        sr=sr,
        hop_length=hop_length,
        y_axis='log',
        x_axis='time',
        cmap='viridis',
        vmin=-80, # Minimum dB value for color mapping
        vmax=0    # Maximum dB value for color mapping
    )

    img1 = librosa.display.specshow(librosa.amplitude_to_db(original_mag), ax=ax1, **kwargs)
    ax1.set_title('Original Spectrogram')
    fig.colorbar(img1, ax=ax1, format='%+2.0f dB')

    img2 = librosa.display.specshow(librosa.amplitude_to_db(modified_mag), ax=ax2, **kwargs)
    ax2.set_title('Watermarked Spectrogram')
    fig.colorbar(img2, ax=ax2, format='%+2.0f dB')

    plt.tight_layout()
    plt.show()

def get_input_file_path(prompt_text, default_filename=None):
    """
    Prompts the user for an input file path, handling relative and absolute paths
    and attempting autodetection with a default filename.

    Args:
        prompt_text (str): The text to display to the user.
        default_filename (str, optional): The default filename to try for autodetection.

    Returns:
        str: The absolute path to the file, or None if an error occurs or file not found.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if default_filename:
        autodetect_path = os.path.join(script_dir, default_filename)
        if os.path.exists(autodetect_path):
            print(f"Autodetected {prompt_text} file at: {autodetect_path}")
            return autodetect_path

    while True:
        location_choice = input(f"Is the {prompt_text} file in the same location as this script? (yes/no): ").lower()
        if location_choice in ['yes', 'y']:
            file_name = input(f"Enter the exact name of the {prompt_text} file (including extension): ")
            file_path = os.path.join(script_dir, file_name)
            if os.path.exists(file_path):
                return file_path
            else:
                print(f"File not found at: {file_path}. Please try again.")
        elif location_choice in ['no', 'n']:
            file_path = input(f"Enter the full path to the {prompt_text} file: ")
            if os.path.exists(file_path):
                return file_path
            else:
                print(f"File not found at: {file_path}. Please try again.")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def watermark_audio(audio_path, watermark_path, output_filename="watermarked_audio.wav"):
    """
    Performs the audio watermarking process.

    Args:
        audio_path (str): Path to the input audio file.
        watermark_path (str): Path to the watermark image file.
        output_filename (str): The desired filename for the watermarked output audio file.
                               The file will be saved in the same directory as the script.
    """
    y, sr, stft, mag, phase = load_and_stft(audio_path)
    if y is None: # Check if loading audio failed
        return

    watermark_mask, freq_start, freq_end = prepare_watermark(watermark_path, mag.shape, sr)
    if watermark_mask is None: # Check if preparing watermark failed
        return

    # Pass the attenuation factor to control the visibility
    modified_mag = embed_watermark(mag, watermark_mask, freq_start, freq_end, attenuation_factor=0.05) # Adjusted attenuation factor

    # Combine the modified magnitude with the original phase to create the modified STFT
    modified_stft = modified_mag * phase

    # Convert the modified STFT back to an audio time series
    modified_audio = librosa.istft(modified_stft)

    # Normalize the audio to prevent clipping
    modified_audio = librosa.util.normalize(modified_audio)

    # Determine the output path in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_filename)

    try:
        # Write the watermarked audio to the output file
        sf.write(output_path, modified_audio, sr)
        print(f"Watermarked audio saved to: {output_path}")
    except Exception as e:
        print(f"Error saving watermarked audio: {e}")
        return

    # Visualize the spectrograms (optional, but good for verification)
    visualize_spectrograms(mag, modified_mag, sr)


if __name__ == "__main__":
    print("--- Audio Watermarking Script ---")

    # Get input audio file path from the user with autodetection
    audio_path = get_input_file_path("input audio", default_filename="input_audio.wav")
    if audio_path is None:
        print("Failed to get input audio file path. Exiting.")
    else:
        # Get watermark image file path from the user with autodetection
        watermark_path = get_input_file_path("watermark image", default_filename="watermark.png")
        if watermark_path is None:
            print("Failed to get watermark image file path. Exiting.")
        else:
            # Perform the watermarking, specifying the output filename
            watermark_audio(audio_path, watermark_path, output_filename="watermarked_audio.wav")

    print("--- Script Finished ---")
