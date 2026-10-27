import { Config } from "@remotion/cli/config";
if (process.env.BROWSER) Config.setBrowserExecutable(process.env.BROWSER);
Config.setVideoImageFormat("png");
