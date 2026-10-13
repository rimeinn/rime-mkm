#!/usr/bin/env python3
"""Run the real MKM processor stack in an isolated directory (requires PyYAML).

Example, after cloning rime-moran (trad), rime-kagiroi and rime-mungyeong:
  python tools/test_mkm.py --mira /path/to/mira \
      --moran /path/to/rime-moran --mungyeong /path/to/rime-mungyeong \
      --kagiroi /path/to/rime-kagiroi
"""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("mira", "moran", "mungyeong", "kagiroi"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="mkm-test-") as temporary:
        work = Path(temporary)
        data = work / "data"
        data.mkdir()
        for repo in (args.moran, args.kagiroi, args.mungyeong, root):
            files = subprocess.check_output(
                ["git", "-C", str(repo), "ls-files", "-z"]
            ).decode().split("\0")
            for name in filter(None, files):
                relative = Path(name)
                if (name.startswith(("lua/", "opencc/")) or
                        (len(relative.parts) == 1 and relative.suffix in (".yaml", ".txt"))):
                    target = data / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(repo / relative, target)

        def patch_file(name, update):
            path = data / name
            document = yaml.safe_load(path.read_text())
            update(document)
            path.write_text(yaml.safe_dump(document, allow_unicode=True, sort_keys=False))

        # Consume the same patches as Plum; keep optional user patches last.
        recipe = yaml.safe_load((root / "recipe.yaml").read_text())
        for name, patch in recipe["patch_files"].items():
            def apply_recipe_patch(doc, patch=patch):
                if isinstance(patch, list):
                    doc["__patch"] = patch
                else:
                    for key, value in patch.items():
                        parent = doc
                        parts = key.split("/")
                        for part in parts[:-1]:
                            parent = parent.setdefault(part, {})
                        parent[parts[-1]] = value
            patch_file(name, apply_recipe_patch)

        patch_file("default.yaml", lambda doc: doc.update({"schema_list": [
            {"schema": name} for name in ("moran", "kagiroi", "mungyeong")
        ]}))
        suites = [*sorted((root / "tests").glob("*.test.yaml")),
                  args.kagiroi / "tests/kagiroi.test.yaml",
                  args.mungyeong / "tests/mungyeong.test.yaml"]
        failed = False
        for index, suite in enumerate(suites):
            spec = yaml.safe_load(suite.read_text())
            spec["source_dir"] = str(data)
            test_file = work / f"suite-{index}.yaml"
            test_file.write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False))
            # An empty cwd avoids reusing any checkout's prebuilt data.
            result = subprocess.run([str(args.mira.resolve()), "-C", str(work / "build"),
                                     str(test_file)], cwd=work)
            failed = failed or result.returncode != 0
        return int(failed)



if __name__ == "__main__":
    raise SystemExit(main())
