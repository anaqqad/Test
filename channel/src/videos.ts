// Register every video's JSON here. Each entry becomes a video composition and a "-thumb" still.
import { VideoSchema, type Video } from "./schema";
import koreanWar from "../data/videos/korean-war.json";
import mongolEmpire from "../data/videos/mongol-empire.json";

export const videos: Video[] = [koreanWar, mongolEmpire].map((v) => VideoSchema.parse(v));
