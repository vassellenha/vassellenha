# Install on GitHub

1. Open `vassellenha/vassellenha` and delete the old `assets/` folder. The new README doesn't use any of those files.
2. Choose **Add file > Upload files** and drag in `README.md` and the `assets` folder together so the folder path stays intact.
3. Commit.

You should end up with:

```text
README.md
assets/
  hero-dark.svg
  hero-light.svg
```

GitHub picks the dark or light hero to match each visitor's theme. The branch draws itself once when the page loads, then a few petals drift down. Visitors who set reduced motion in their OS get the finished branch with nothing moving.

Delete this INSTALL.md after uploading if you don't want it in the repo.
