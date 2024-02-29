import json
import os
import pathlib
import tarfile
import urllib.request

flet_web_job_name = "Build Flet for web"

build_jobs = {}


def download_flet_web(jobId, dest_file):
    flet_web_url = f"https://ci.appveyor.com/api/buildjobs/{jobId}/artifacts/client/build/flet-web.tar.gz"
    print(f"Downloading {flet_web_url}...")
    urllib.request.urlretrieve(flet_web_url, dest_file)


def get_flet_server_job_ids():
    account_name = os.environ.get("APPVEYOR_ACCOUNT_NAME")
    project_slug = os.environ.get("APPVEYOR_PROJECT_SLUG")
    build_id = os.environ.get("APPVEYOR_BUILD_ID")
    url = f"https://ci.appveyor.com/api/projects/{account_name}/{project_slug}/builds/{build_id}"
    print(f"Fetching build details at {url}")
    req = urllib.request.Request(url)
    req.add_header("Content-type", "application/json")
    project = json.loads(urllib.request.urlopen(req).read().decode())
    for job in project["build"]["jobs"]:
        build_jobs[job["name"]] = job["jobId"]


current_dir = pathlib.Path(os.getcwd())
print("current_dir", current_dir)

get_flet_server_job_ids()

# create "web" directory
web_path = current_dir.joinpath("src", "flet", "web")
web_path.mkdir(exist_ok=True)
web_tar_path = current_dir.joinpath("flet-web.tar.gz")
download_flet_web(build_jobs[flet_web_job_name], web_tar_path)
with tarfile.open(web_tar_path, "r:gz") as tar:
    tar.extractall(str(web_path))
os.remove(web_tar_path)
