// Register every video's JSON here. Each entry becomes a video composition and a "-thumb" still.
import { VideoSchema, type Video } from "./schema";
import koreanWarDemo from "../data/videos/korean-war-demo.json";

export const videos: Video[] = [koreanWarDemo].map((v) => VideoSchema.parse(v));
