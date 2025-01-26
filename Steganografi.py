import cv2
import wave
import os
from PIL import Image
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import gzip
import argparse
import time
from pathlib import Path

# ==================== PENGATURAN LOGGING ====================
logging.basicConfig(filename='steganography.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# ==================== FUNGSI EMAIL PERINGATAN ====================

def send_email_alert(subject, message):
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    password = "your_email_password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            logging.info("Email peringatan terkirim.")
    except Exception as e:
        logging.error(f"Gagal mengirim email: {e}")

# ==================== FUNGSI STEGANOGRAFI ====================

# Fungsi untuk menyisipkan teks pendek ke gambar
def encode_image(input_image_path, output_image_path, secret_message):
    img = Image.open(input_image_path)
    img_array = np.array(img)

    # Kompresi pesan dan konversi menjadi biner
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'  # Terminator
    binary_message = gzip.compress(binary_message.encode('utf-8')).decode('latin1')

    # Modifikasi piksel gambar untuk menyisipkan data
    idx = 0
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(3):  # Setiap channel (RGB)
                if idx < len(binary_message):
                    img_array[i, j, k] = (img_array[i, j, k] & ~1) | int(binary_message[idx])
                    idx += 1

    # Simpan gambar dengan pesan tersembunyi
    encoded_img = Image.fromarray(img_array)
    encoded_img.save(output_image_path)
    logging.info(f"Teks berhasil disembunyikan dalam gambar {output_image_path}")
    send_email_alert("Steganografi - Pesan Tersimpan", f"Teks berhasil disembunyikan dalam gambar {output_image_path}")

# Fungsi untuk mengekstrak teks dari gambar
def decode_image(image_path):
    img = Image.open(image_path)
    img_array = np.array(img)

    binary_message = ""
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(3):
                binary_message += str(img_array[i, j, k] & 1)

    # Konversi biner ke teks hingga menemukan terminator
    binary_message = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
    secret_message = ''.join([chr(int(byte, 2)) for byte in binary_message])
    decoded_message = secret_message.split(chr(0xFF) + chr(0xFE))[0]  # Menghentikan pada terminator
    decoded_message = gzip.decompress(decoded_message.encode('latin1')).decode('utf-8')
    print("Pesan tersembunyi:", decoded_message)

# ==================== STEGANOGRAFI UNTUK AUDIO ====================

# Fungsi untuk menyisipkan teks sedang ke dalam audio
def encode_audio(input_audio_path, output_audio_path, secret_message):
    audio = wave.open(input_audio_path, 'rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    # Kompresi pesan dan konversi menjadi biner
    secret_message += '###'
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    binary_message = gzip.compress(binary_message.encode('utf-8')).decode('latin1')

    if len(binary_message) > len(frame_bytes):
        raise ValueError("Pesan terlalu besar untuk file audio ini!")

    for i in range(len(binary_message)):
        frame_bytes[i] = (frame_bytes[i] & 254) | int(binary_message[i])

    # Simpan file audio baru dengan data tersembunyi
    modified_audio = wave.open(output_audio_path, 'wb')
    modified_audio.setparams(audio.getparams())
    modified_audio.writeframes(frame_bytes)
    modified_audio.close()
    audio.close()
    logging.info(f"Teks berhasil disembunyikan dalam audio {output_audio_path}")
    send_email_alert("Steganografi - Pesan Tersimpan", f"Teks berhasil disembunyikan dalam audio {output_audio_path}")

# Fungsi untuk mengekstrak teks dari audio
def decode_audio(audio_path):
    audio = wave.open(audio_path, 'rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    extracted_bits = [str(frame_bytes[i] & 1) for i in range(len(frame_bytes))]
    binary_message = ''.join(extracted_bits)
    binary_message = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
    secret_message = ''.join([chr(int(byte, 2)) for byte in binary_message])
    decoded_message = secret_message.split('###')[0]
    decoded_message = gzip.decompress(decoded_message.encode('latin1')).decode('utf-8')
    print("Pesan tersembunyi:", decoded_message)
    audio.close()

# ==================== STEGANOGRAFI UNTUK VIDEO ====================

# Fungsi untuk menyisipkan data besar ke video
def encode_video(input_video_path, output_video_path, secret_message):
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS), 
                          (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
    secret_message += '###'
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    binary_message_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or binary_message_index >= len(binary_message):
            break

        for row in frame:
            for pixel in row:
                if binary_message_index < len(binary_message):
                    pixel[0] = (pixel[0] & ~1) | int(binary_message[binary_message_index])
                    binary_message_index += 1
        out.write(frame)

    cap.release()
    out.release()
    logging.info(f"Data besar berhasil disembunyikan dalam video {output_video_path}")
    send_email_alert("Steganografi - Data Tersimpan", f"Data besar berhasil disembunyikan dalam video {output_video_path}")

# Fungsi untuk mengekstrak data besar dari video
def decode_video(video_path):
    cap = cv2.VideoCapture(video_path)
    binary_message = ""

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for row in frame:
            for pixel in row:
                binary_message += str(pixel[0] & 1)

    cap.release()

    binary_message = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
    secret_message = ''.join([chr(int(byte, 2)) for byte in binary_message])
    decoded_message = secret_message.split('###')[0]
    decoded_message = gzip.decompress(decoded_message.encode('latin1')).decode('utf-8')
    print("Data besar tersembunyi:", decoded_message)

# ==================== FUNGSI UTAMA ====================

def main():
    parser = argparse.ArgumentParser(description="Steganografi Multiformat")
    parser.add_argument("operation", choices=["encode_image", "decode_image", "encode_audio", "decode_audio", "encode_video", "decode_video"], 
                        help="Operasi yang ingin dilakukan")
    parser.add_argument("input_file", type=str, help="File input (gambar/audio/video)")
    parser.add_argument("output_file", type=str, help="File output")
    parser.add_argument("message", type=str, help="Pesan yang akan disembunyikan (untuk encoding)")
    
    args = parser.parse_args()

    if args.operation == "encode_image":
        encode_image(args.input_file, args.output_file, args.message)
    elif args.operation == "decode_image":
        decode_image(args.input_file)
    elif args.operation == "encode_audio":
        encode_audio(args.input_file, args.output_file, args.message)
    elif args.operation == "decode_audio":
        decode_audio(args.input_file)
    elif args.operation == "encode_video":
        encode_video(args.input_file, args.output_file, args.message)
    elif args.operation == "decode_video":
        decode_video(args.input_file)

if __name__ == "__main__":
    main()
