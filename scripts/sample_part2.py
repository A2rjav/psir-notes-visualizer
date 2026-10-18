import os

# We can inspect page filenames and quick sample
for p in [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 150]:
    fn = f"page_{p:03d}.png"
    fp = os.path.join("scans_paper1_part2", fn)
    print(f"Page {p}: exists={os.path.exists(fp)}, size={os.path.getsize(fp)}")
