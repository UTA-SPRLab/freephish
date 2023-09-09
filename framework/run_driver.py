import logging
from concurrent.futures import ThreadPoolExecutor
from data_collection import get_twitter, get_fb
from detection_calls import test
from blocklist_measurement import activity_measurement, blocklist_measurement, vt_measurement
from disclosure_framework import disclosure_fwb
from parser import web_parser
from filelock import FileLock

logging.basicConfig(filename='main_driver.log', level=logging.INFO)
lock = FileLock("main_driver.log.lock")

def run_module(fn, *args):
    try:
        fn(*args)
        with lock:
            logging.info(f"Successfully ran {fn.__name__}")
    except Exception as e:
        with lock:
            logging.error(f"Failed to run {fn.__name__}: {e}")

# List of function configurations
functions_with_args = [
    (get_twitter.get_twitter_posts,),
    (get_fb.get_fb_posts,),
    (web_parser,),
    (test.predict_parser,),
    (activity_measurement.check_url_activity, "urls.csv"),
    (blocklist_measurement.check_urls, "urls.csv", "urls_temp.csv"),
    (vt_measurement.run_virustotal, "urls.csv", 20000),
    (disclosure_fwb.disclose_urls,)
]

# Run all functions in parallel
with ThreadPoolExecutor() as executor:
    for func_config in functions_with_args:
        executor.submit(run_module, *func_config)
