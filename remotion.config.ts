/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setJpegQuality(92);
Config.setOverwriteOutput(true);
Config.setCodec("h264");
Config.setCrf(18);

// Use a locally installed Chrome Headless Shell when Remotion cannot download its own
// (e.g. sandboxed CI). Override with REMOTION_BROWSER_EXECUTABLE=/path/to/headless_shell.
import fs from "node:fs";

const localBrowser = [
  process.env.REMOTION_BROWSER_EXECUTABLE,
  "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
].find((p): p is string => Boolean(p) && fs.existsSync(p as string));
if (localBrowser) {
  Config.setBrowserExecutable(localBrowser);
}
