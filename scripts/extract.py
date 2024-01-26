import argparse
from dataclasses import dataclass
from pathlib import Path
import gzip
import json


@dataclass
class Args(object):
    input: list[Path]
    output: Path
    lines: int

    @staticmethod
    def parse() -> "Args":
        script_dir = Path(__file__).parent

        p = argparse.ArgumentParser()
        p.add_argument("--output", type=Path, default=script_dir.parent / "examples")
        p.add_argument("input", type=Path, nargs="+")
        p.add_argument("--lines", type=int, default=100)
        return Args(**vars(p.parse_args()))


def process_file(inf, outf, args: Args, limit: int):
    count = 0
    for line in inf:
        obj = json.loads(line)
        res = {}
        # enforce specific field order (requires Python 3.7+)
        res["text"] = obj["text"]
        res["url"] = obj["url"]
        res["docId"] = obj["docId"]
        res["date"] = obj["date"]
        res["charset"] = obj["charset"]
        json.dump(res, outf, ensure_ascii=False)
        outf.write("\n")
        count += 1
        if count >= limit:
            break
    return count


def process(args: Args):
    remaining = args.lines
    for inp in args.input:
        inp = inp.resolve()
        with inp.open("rb") as inf:
            if inp.name.endswith(".gz"):
                inf = gzip.open(inf)
            inp_parent = inp.parent
            outf_name = inp_parent.name + ".txt"
            outf_name = args.output / outf_name
            with outf_name.open("at") as outf:
                remaining -= process_file(inf, outf, args, remaining)
        if remaining <= 0:
            break


if __name__ == "__main__":
    args = Args.parse()
    args.output.mkdir(exist_ok=True, parents=True)
    process(args)
