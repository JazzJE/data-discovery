import subprocess

from config import Config


FLOWER_SCRIPT = (
	Config.FolderPaths.ROOT
	/ "external"
	/ "FlowER-repo"
	/ "run_FlowER_large_newData.sh"
)


def run_flower() -> None:
	"""Run the FlowER inference shell script from the project root."""
	if not FLOWER_SCRIPT.is_file():
		raise FileNotFoundError(f"FlowER launcher not found: {FLOWER_SCRIPT}")

	subprocess.run(
		["bash", str(FLOWER_SCRIPT)],
		cwd=FLOWER_SCRIPT.parent,
		check=True,
	)


if __name__ == "__main__":
	run_flower()
