# python imports
import os
from dotenv import load_dotenv

# local imports
from fuga.api_client import FUGAClient
from fuga.miscellaneous import FUGAMisc

# set variables
load_dotenv()  # Load environment variables from .env file
API_URL = os.getenv("API_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Initialize the FUGA API client
client = FUGAClient(API_URL, USERNAME, PASSWORD)
client.login()

path = "/error_messages/upload"

res = client.request("GET", path)

print(f"Response: {res}")


errors_uploads = {
    "AUDIO_BIT_DEPTH_INVALID": "Invalid audio Bit Depth",
    "AUDIO_CHANNEL_INVALID": "Invalid audio channels",
    "AUDIO_DURATION_IS_ZERO": "Duration is zero",
    "AUDIO_FLOATING_POINT_WAV": "Floating point WAV file",
    "AUDIO_INVALID_CODEC": "Invalid Audio codec",
    "AUDIO_INVALID_DSD_FILE": "Invalid DSD file",
    "AUDIO_INVALID_FLAC_FILE": "Invalid or corrupted FLAC",
    "AUDIO_INVALID_STEMS_FILE": "Invalid STEMS file",
    "AUDIO_SAMPLING_RATE_INVALID": "Invalid audio Sampling Rate",
    "AUDIO_SANITIZATION_ERROR": "Failed to sanitize audio file",
    "AUDIO_UPLOADED_IS_A_VIDEO": "Uploaded file is a video",
    "AUDIO_WAV_TO_FLAC_ERROR": "Failed to convert WAV to FLAC",
    "CHECKSUM_MISSING_FILE_ERROR": "File is missing",
    "CHECKSUM_ZERO_BYTE_ERROR": "File size is zero bytes",
    "CHUNK_UPLOAD_BAD_CONTENT_BODY": "Invalid content body",
    "CHUNK_UPLOAD_MISSING_PARAMETERS": "Missing parameters",
    "CHUNK_UPLOAD_MULTIPLE_CHUNKS_OPENED": "Maximum file multiparts in content reached",
    "CHUNK_UPLOAD_NEGATIVE_OFFSET": "Offset is negative",
    "DOLBY_ATMOS_INVALID_ADM_PROFILE": "Invalid ADM profile",
    "DOLBY_ATMOS_INVALID_BIT_DEPTH": "Invalid bit depth",
    "DOLBY_ATMOS_INVALID_CHANNELS": "Invalid number of channels",
    "DOLBY_ATMOS_INVALID_FORMAT": "Invalid format",
    "DOLBY_ATMOS_INVALID_SAMPLING_RATE": "Invalid sampling rate",
    "DOWNLOAD_FOUND": "Found",
    "DOWNLOAD_SOURCE_FILE_NOT_FOUND": "Source file not found",
    "EXISTING_UPLOAD_NOT_FOUND": "Existing upload information not found",
    "IMAGE_CHUNK_DATA_TOO_LARGE": "Image contains huge metadata information",
    "IMAGE_CORRUPTED_ERROR": "Invalid or corrupted image",
    "IMAGE_COVER_ART_ABOVE_MAXIMUM_DIMENSIONS": "Cover art dimensions must be at most 8000x8000",
    "IMAGE_COVER_ART_BELOW_MINIMUM_DIMENSIONS": "Cover art dimensions must be at least 1400x1400",
    "IMAGE_FAILED_TO_EXTRACT_METADATA_ERROR": "Unable to extract image metadata",
    "IMAGE_INVALID_MIME_TYPE_ERROR": "Invalid image mime type",
    "INVALID_OR_CORRUPT_FILE_UPLOADED": "File uploaded is corrupted or invalid",
    "MOTION_ART_INVALID_CODEC_ERROR": "Video codec not supported",
    "MOTION_ART_INVALID_COLOR_SPACE": "Invalid video colorspace",
    "MOTION_ART_INVALID_DURATION": "Invalid video duration",
    "MOTION_ART_INVALID_FRAME_RATE": "Invalid video frame rate",
    "MOTION_ART_INVALID_VIDEO_RESOLUTION": "Invalid video resolution",
    "REQUEST_INVALID_FORMAT_PARAMETER": "Invalid format parameter",
    "REQUEST_INVALID_TOKEN_ERROR": "Invalid token in request",
    "REQUEST_MISSING_DOMAIN_ERROR": "Missing domain parameter",
    "REQUEST_MISSING_SESSION_ID": "Missing id parameter",
    "REQUEST_MISSING_TOKEN_ERROR": "Missing token in request",
    "SYSTEM_ERROR": "System Error",
    "SYSTEM_ERROR_GENERIC": "System Error",
    "SYSTEM_ERROR_INVALID_PARAM_TYPE": "Invalid parameter type",
    "SYSTEM_ERROR_INVALID_UPLOAD_FORMAT": "Format not supported",
    "SYSTEM_ERROR_METADATA_EXTRACTION": "Metadata extraction error",
    "SYSTEM_INVALID_REQUEST_PARAMETERS": "Invalid parameters format",
    "SYSTEM_PATH_NOT_FOUND": "Path not found",
    "UPLOAD_CHECKSUM_DOES_NOT_MATCH": "Uploaded file checksum does not match",
    "UPLOAD_FAILED_EXTRACTING_TOKEN": "Failed extracting token",
    "UPLOAD_FAILED_TO_VALIDATE_FILE": "Failed to validate file",
    "UPLOAD_FILE_HAS_ZERO_BYTES": "Uploaded file has zero bytes",
    "UPLOAD_MISSING_CHUNK_SIZE": "Missing chunk size parameter",
    "UPLOAD_UNKNOWN_TOKEN_MESSAGE_TYPE": "Unknown token message type",
    "VIDEO_FRAME_RATE_NOT_DETECTED": "Video frame rate could not be detected",
    "VIDEO_INVALID_CODEC_ERROR": "Video codec not supported",
    "VIDEO_INVALID_FRAME_RATE": "Video frame rate must be at least 15",
    "VIDEO_INVALID_VIDEO_RESOLUTION": "Video resolution must be at least 320x100",
    "MOTION_ART_SCAN_TYPE_INVALID": "Invalid Video Scan Type. Only Progressive Scan type is accepted.",
    "AUDIO_INVALID_DSD_FILE_SAMPLING_RATE": "Invalid DSD file sampling rate",
    "AUDIO_INVALID_DSD_FILE_BIT_DEPTH": "Invalid DSD file bit depth",
    "AUDIO_INVALID_DSD_FILE_CHANNELS": "Invalid DSD file channels",
    "IMAGE_COVER_ART_HEIGHT_BELOW_MINIMUM_DIMENSIONS": "Cover art height below minimum size",
    "IMAGE_COVER_ART_WIDTH_BELOW_MINIMUM_DIMENSIONS": "Cover art width below minimum size",
    "IMAGE_COVER_ART_HEIGHT_ABOVE_MAXIMUM_DIMENSIONS": "Cover art height above maximum size",
    "IMAGE_COVER_ART_WIDTH_ABOVE_MAXIMUM_DIMENSIONS": "Cover art width above maximum size",
    "MOTION_ART_INVALID_VIDEO_RESOLUTION_HEIGHT": "Invalid motion art video resolution height",
    "MOTION_ART_INVALID_VIDEO_RESOLUTION_WIDTH": "Invalid motion art video resolution width",
    "VIDEO_INVALID_VIDEO_RESOLUTION_HEIGHT": "Invalid video resolution height",
    "VIDEO_INVALID_VIDEO_RESOLUTION_WIDTH": "Invalid video resolution width",
    "CHUNK_UPLOAD_MISSING_PARAMETER_UUID": "Missing parameter: uuid",
    "CHUNK_UPLOAD_MISSING_PARAMETER_FILE_NAME": "Missing parameter: filename",
    "CHUNK_UPLOAD_MISSING_PARAMETER_PART_BYTE_OFFSET": "Missing parameter: partbyteoffset",
    "REQUEST_NOT_A_MULTIPART_UPLOAD": "Request is not a multipart upload request",
    "INVALID_CHUNK_UPLOAD_SESSION_ID": "Session ID contains illegal characters",
    "AUDIO_WAV_TO_FLAC_DURATION_MISMATCH_ERROR": "Converted flac file duration did not match the original wav file",
    "ATTACHMENT_INVALID_FILE_TYPE": "Detected file type is not allowed",
    "MOTION_ART_AUDIO_CHANNELS_DETECTED": "Motion Art contains audio channels",
}
