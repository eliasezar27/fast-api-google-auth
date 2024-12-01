import logging
import sys
import time
from functools import wraps
from fastapi import Request
from logging.handlers import RotatingFileHandler


# Set logger time zone to UTC
logging.Formatter.converter = time.gmtime

# Get logger
logger = logging.getLogger()

# Log format
formatter = logging.Formatter(
    fmt="%(levelname)s:\t  %(asctime)s - route: (%(name)s) - %(message)s"
)

# Stream handler to print logs to stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Rotating file handler with max file size and backup files
file_handler = RotatingFileHandler(
    'app.log',  # Log file path
    maxBytes=10 * 1024 * 1024,  # 10 MB size limit
    backupCount=3  # Keep 3 backup log files
)
file_handler.setFormatter(formatter)

# Apply handlers to logger
logger.handlers = [stream_handler, file_handler]
logger.setLevel(logging.INFO)

def log_execution_time(func):
    '''
    Wrapper function that logs execution time of a triggered route.
    '''
    
    @wraps(func)
    async def wrapper(request: Request = None, *args, **kwargs):
        start_time = time.time()
        logger.setLevel(logging.INFO)
        logger.name = request.url.path
        try:
            result = await func(request, *args, **kwargs)  # Execute the actual route handler
        except Exception as e:
            # Log the error
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"Executed for: {execution_time:.4f} seconds")
            logger.error(f"Error: {str(e)}", exc_info=True)
            raise e  # Re-raise the exception after logging execution time
        else:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"Executed for: {execution_time:.4f} seconds")
        
        return result
    return wrapper