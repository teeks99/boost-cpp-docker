import sys
import subprocess
import datetime
import argparse
import re

options = None
push_log = {"versions":{}}

versions = [
    # Precise
    # "gcc-4.4", "gcc-4.5",
    # Trusty
    # "clang-2.9", "clang-3.0", "clang-3.1", "clang-3.2", "clang-3.3",
    # "clang-3.4", "clang-3.5", "clang-3.6", "clang-3.7", "clang-3.8",
    # "gcc-4.6", "gcc-4.7", "gcc-4.8", "gcc-4.9", "gcc-5", "gcc-6",
    # Xenial
    "clang-3.9", "clang-4", "clang-5", "clang-6",
    "gcc-7",
    # Bionic
    "clang-7", "clang-8", "clang-9", "clang-10",
    "gcc-8",
    # Focal
    "clang-11", "clang-12", "clang-13", "clang-14",
    "gcc-9", "gcc-10", "gcc-11",
    # Jammy
    "clang-15", "clang-16", "clang-16",
    "gcc-12", "gcc-13"
    ]

test_versions = {}

class Image(object):
    def __init__(self, repo, tag):
        self.repo = repo
        self.tag = tag

    @property
    def image(self):
        return f"{self.repo}:{self.tag}"


def run_my_cmd(cmd):
    try:
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    except Exception:
        print("Failure in command: " + cmd)
        raise

def build(version):
    image = Image(options.repo, version)

    force = "--no-cache"
    if options.no_force:
        force = ""

    cmd = f"docker build {force} --tag {image.image} {version}"
    run_my_cmd(cmd)
    return image


def test(image, test_version):
    pass


def tag_timestamp(base_image, version):
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M")
    tag = f"{version}_{timestamp}"
    image = Image(options.repo, tag)
    cmd = f"docker tag {base_image.image} {image.image}"
    run_my_cmd(cmd)
    return image


def tag_latest(base_image):
    image = Image(options.repo,"latest")
    cmd = f"docker tag {base_image.image} {image.image}"
    run_my_cmd(cmd)
    return image


def push_image(image):
    cmd = f"docker push {image.image}"
    run_my_cmd(cmd)


def create_and_push_manifest(time_image, version_tag):
    manifest_image = Image(options.repo, version_tag)
    cmd = f"docker manifest rm {manifest_image.image}"
    try:
        run_my_cmd(cmd)
    except subprocess.CalledProcessError:
        pass

    cmd = f"docker manifest create {manifest_image.image}"
    cmd += f" --amend {time_image.image}"
    for additional in options.manifest_add:
        cmd += f" --amend {options.repo}:{additional}"
    run_my_cmd(cmd)

    cmd = f"docker manifest push {manifest_image.image}"
    run_my_cmd(cmd)


def remove_image(image):
    cmd = f"docker rmi {image.image}"
    run_my_cmd(cmd)


def all():
    for version in versions:
        latest = False
        if options.latest and version == versions[-1]:
            latest = True
        build_one(version, latest)


def build_one(version, push_latest=False):
    tags = []
    base_image = None
    time_image = None
    latest_image = None

    if not options.no_build:
        base_image = build(version)

    if not options.no_test:
        tv = version
        if version in test_versions:
            tv = test_versions[version]

        test(base_image, tv)

    if not options.no_tag_timestamp:
        time_image = tag_timestamp(base_image, version)

    if push_latest:
        if not options.manifest_add:
            latest_image = tag_latest(base_image)

    if options.no_push_tag or options.manifest_add:
        base_image = None

    if options.push:
        for img in (base_image, time_image, latest_image):
            if img:
                push_image(img)

        pushes = {}
        if base_image:
            pushes["base"] = base_image.tag
        if time_image:
            pushes["timestamp"] = time_image.tag
        if latest_image:
            pushes["latest"] = True
        push_log["versions"][version] = pushes

    if options.manifest_add:
        create_and_push_manifest(time_image, version)
        if push_latest:
            create_and_push_manifest(time_image, "latest")

    if options.delete_timestamp_tag:
        remove_image(time_image)


def set_options():
    parser = argparse.ArgumentParser(
        description="Build one or more docker images for boost-cpp-docker")
    parser.add_argument(
        "-v", "--version", action="append",
        help="Use one of more times to specify the versions to run, skip"
        + " for all")
    parser.add_argument(
        "--no-build", action="store_true", help="skip build step")
    parser.add_argument(
        "--no-force", action="store_true",
        help="don't force an update, use existing layers")
    parser.add_argument(
        "--no-test", action="store_true", help="skip the test step")
    parser.add_argument(
        "--no-tag-timestamp", action="store_true", help="only version tag")
    parser.add_argument(
        "--latest", action="store_true",
        help="Update latest tag. If multiple versions, applies to last one." +
        " If --manifest-add specified will create a latest manifest")
    parser.add_argument(
        "-T", "--no-push-tag", action="store_true",
        help="Do not apply the tag for the version, only the timestamp tag")
    parser.add_argument(
        "-r", "--repo", default="test/boost-cpp",
        help="repo to build for and push to. Defaults to test/boost-cpp, " +
        "use teeks99/boost-cpp-docker for dockerhub")
    parser.add_argument(
        "-p", "--push", action="store_true", help="push to dockerhub")
    parser.add_argument(
        "-d", "--delete-timestamp-tag", action="store_true",
        help="remove the timestamp tag from the local machine")
    parser.add_argument(
        "-m", "--manifest-add", action="append",
        help="Generate a manifest for the version supplied, using the" +
        " timestamp upload as the first version add the timestamp(s)" +
        " specified here as additional versions. Used for generating" + 
        " multiarch images on different machines.")
    parser.add_argument(
        "-l", "--log-file", default="",
        help="json file to log pushes into")

    global options
    options = parser.parse_args()

    if options.manifest_add and len(options.version) > 1:
        raise RuntimeError("Cannot support manifest with multiple versions")


def run():
    set_options()
    push_log["repo"] = options.repo

    if options.version:
        global versions
        versions = options.version

    all()

    if options.log_file:
        with open(options.log_file, "w") as f:
            json.dump(push_log, f)


if __name__ == "__main__":
    run()
