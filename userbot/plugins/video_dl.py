import asyncio
import os
import re
import subprocess
import tempfile

import requests
from pyrogram import filters
from pyrogram.types import Message, LinkPreviewOptions

from userbot import UserBot, SOCKS5_PROXY
from userbot.plugins.help import add_command_help

# Instagram URL regex pattern - updated to include ddinstagram.com
instagram_regex = r'https?://(www\.)?(instagram\.com|ddinstagram\.com)/(p|reels|reel|tv|stories)/[a-zA-Z0-9_-]+/?'

# TikTok URL regex pattern - updated to support empty usernames
tiktok_regex = r'https?://(www\.|vm\.|vt\.)?tiktok\.com/(@[\w.-]*/video/\d+|@/video/\d+|[\w]+/?).*'

# Combined regex for function trigger
video_url_regex = f"({instagram_regex}|{tiktok_regex})"


def get_final_url(url):
    """Get the final URL by following redirects and cleaning it"""
    try:
        # Create a session that follows redirects
        session = requests.Session()

        # Make HEAD request to get redirect without downloading content
        response = session.head(url, allow_redirects=True)

        if response.status_code == 200:
            # Get the final URL after all redirects
            final_url = response.url

            # Remove tracking parameters (anything after the ?)
            clean_url = final_url.split('?')[0]

            return clean_url

    except Exception:
        pass

    # Return original if anything fails
    return url


def process_urls(url):
    """Process URLs for both Instagram and TikTok"""
    # First, follow redirects to get the real URL
    real_url = get_final_url(url)

    # For ddinstagram.com links, always convert to instagram.com
    if "ddinstagram.com" in real_url:
        download_url = real_url.replace("ddinstagram.com", "instagram.com")
    else:
        download_url = real_url

    return download_url

@UserBot.on_message(filters.regex(video_url_regex) & filters.me)
async def video_downloader(bot: UserBot, message: Message, from_reply=False):
    # Extract the video URL from the message
    message_text = message.text

    # Don't download if there is additional content in the message
    if not message_text.startswith("http") and not from_reply:
        return

    # Determine which platform URL it is
    if re.search(instagram_regex, message_text):
        platform = "Instagram"
        match = re.search(instagram_regex, message_text)
    elif re.search(tiktok_regex, message_text):
        platform = "TikTok"
        match = re.search(tiktok_regex, message_text)
    else:
        return

    if not match:
        return

    original_url = match.group(0)

    # Process URL to get the download URL and display URL
    download_url = process_urls(original_url)

    # Send a new status message (silently and without preview)
    status_msg = await bot.send_message(
        message.chat.id,
        f"Downloading from {platform}: {download_url}",
        disable_notification=True,  # Send silently
        link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
    )

    # Create a temporary directory for downloading
    with tempfile.TemporaryDirectory() as temp_dir:
        yt_dlp_args = [
            "yt-dlp",
            download_url,
            "-o",
            os.path.join(temp_dir, "%(title)s [%(id)s].%(ext)s")
        ]

        # Use SOCKS5 proxy if configured
        if SOCKS5_PROXY:
            yt_dlp_args.append("--proxy")
            yt_dlp_args.append(SOCKS5_PROXY)

        try:
            # Update status (without preview)
            await status_msg.edit(
                f"⬇️ Downloading: {download_url}",
                link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
            )

            # Download the video using yt-dlp
            process = subprocess.run(
                yt_dlp_args,
                capture_output=True,
                text=True,
                check=False
            )

            if process.returncode != 0:
                await status_msg.edit(
                    f"⚠️ Failed to download: {process.stderr[:500]}...\n\nTrying with different options...",
                    link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
                )

                # Try with --no-check-certificate if it failed
                yt_dlp_args.append('--no-check-certificate')
                process = subprocess.run(
                    yt_dlp_args,
                    capture_output=True,
                    text=True,
                    check=False
                )

                if process.returncode != 0:
                    await status_msg.edit(
                        f"❌ Download failed. Error: {process.stderr[:500]}...",
                        link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
                    )
                    return

            # Get the downloaded file
            downloaded_files = os.listdir(temp_dir)
            if not downloaded_files:
                await status_msg.edit(
                    "❌ No files downloaded.",
                    link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
                )
                return

            video_path = os.path.join(temp_dir, downloaded_files[0])

            # Extract the caption without extension
            file_name = os.path.splitext(downloaded_files[0])[0]

            # Extract title from filename
            if "[" in file_name and "]" in file_name:
                title = file_name.split(" [")[0]
            else:
                title = file_name

            # Create caption with the download URL (which has been cleaned and followed redirects)
            caption = f"{title}\n{download_url}"

            # Update status (without preview)
            await status_msg.edit(
                "⬆️ Uploading video...",
                link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
            )

            # Upload the video (this one can notify as it's the final content)
            await bot.send_video(
                message.chat.id,
                video_path,
                caption=caption
            )
            
            if not from_reply: await message.delete()

            # Delete the status message when complete
            await status_msg.delete()

        except Exception as e:
            await status_msg.edit(
                f"❌ Error: {str(e)[:500]}...",
                link_preview_options=LinkPreviewOptions(is_disabled=True)  # Disable link preview
            )
            await asyncio.sleep(5)
            await status_msg.delete()

@UserBot.on_message(filters.command("dl", ".") & filters.me)
async def download_video_command(bot: UserBot, message: Message):
    """Download the video from the link sent in the message."""
    if not message.reply_to_message or not message.reply_to_message.text:
        await message.edit_text("Please reply to a message containing a video link.")
        return

    # Extract the link from the replied message
    reply_text = message.reply_to_message.text.strip()
    
    # Check if it matches the video URL regex
    if not re.search(video_url_regex, reply_text):
        await message.edit_text("The replied message does not contain a valid video link.")
        return

    # Call the main video downloader function with the link
    await message.delete()
    await video_downloader(bot, message.reply_to_message, from_reply=True)

# Command help section
add_command_help(
    "video_dl",
    [
        [
            "https://instagram.com/reel/... or https://ddinstagram.com/reel/...",
            "Automatically downloads Instagram videos/reels when you send a link and uploads them with a proper caption.",
        ],
        [
            "https://tiktok.com/... or https://vt.tiktok.com/...",
            "Automatically downloads TikTok videos when you send a link and uploads them with the original caption and link.",
        ],
        [
            ".dl",
            "Download the video from the link you sent. This command is useful to trigger it for a link someone else sends.",
        ]
    ],
)
