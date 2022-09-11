import sys
import subprocess
import datetime
import argparse
import re

options = None

versions = [
    # Precise
    # "gcc-4.4", "gcc-4.5",
    # Trusty
    # "clang-2.9", "clang-3.0", "clang-3.1", "clang-3.2", "clang-3.3",
    # "clang-3.4", "clang-3.5", "clang-3.6", "clang-3.7", "clang-3.8",
    "gcc-4.6", "gcc-4.7", "gcc-4.8", "gcc-4.9", "gcc-5", "gcc-6",
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
    "clang-15", "clang-16",
    "gcc-12"
    ]

test_versions = {}


def build(version):
    tag = f"{options.repo}:{version}"

    force = "--no-cache"
    if options.no_force:
        force = ""

    cmd = f"docker build --pull {force} --tag {tag} {version}"
    print(cmd)
    try:
        subprocess.check_call(cmd, shell=True)
    except Exception:
        print("Failure in command: " + cmd)
        raise
    return tag


def test(tag, test_version):
    pass


def tag_timestamp(base_tag, version):
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M")
    tag = f"{options.repo}:{version}_{timestamp}"
    cmd = f"docker tag {base_tag} {tag}"
    try:
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    except Exception:
        print("Failure in command: " + cmd)
        raise
    return tag


def tag_latest(base_tag):
    tag = f"{options.repo}:latest"
    cmd = f"docker tag {base_tag} {tag}"
    try:
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    except Exception:
        print("Failure in command: " + cmd)
        raise
    return tag


def push_tag(tag):
    cmd = f"docker push {tag}"
    try:
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    except Exception:
        print("Failure in command: " + cmd)
        raise


def remove_tag(tag):
    cmd = f"docker rmi {tag}"
    try:
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    except Exception:
        print("Failure in command: " + cmd)
        raise


def all():
    for version in versions:
        build_one(version)


def build_one(version):
    tags = []
    base_tag = None
    time_tag = None
    latest_tag = None

    if not options.no_build:
        base_tag = build(version)

    if not options.no_test:
        tv = version
        if version in test_versions:
            tv = test_versions[version]

        test(base_tag, tv)

    if not options.no_tag_timestamp:
        time_tag = tag_timestamp(base_tag, version)

    if options.latest:
        latest_tag = tag_latest(base_tag)

    if options.push:
        for tag in (base_tag, time_tag, latest_tag):
            if tag:
                push_tag(tag)

    if options.delete_timestamp_tag:
        remove_tag(time_tag)


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
        help="update each to latest tag, whichever version is"
        + " specified last will win")
    parser.add_argument(
        "-r", "--repo", default="test/boost-cpp",
        help="repo to build for and push to. Defaults to test/boost-cpp, " +
        "use teeks99/boost-cpp-docker for dockerhub")
    parser.add_argument(
        "-p", "--push", action="store_true", help="push to dockerhub")
    parser.add_argument(
        "-d", "--delete-timestamp-tag", action="store_true",
        help="remove the timestamp tag from the local machine")

    global options
    options = parser.parse_args()


def run():
    set_options()

    if options.version:
        global versions
        versions = options.version

    all()


if __name__ == "__main__":
    run()
