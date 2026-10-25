// Register every video's JSON here. Each entry becomes a video composition and a "-thumb" still.
import { VideoSchema, type Video } from "./schema";
import koreanWar from "../data/videos/korean-war.json";
import mongolEmpire from "../data/videos/mongol-empire.json";
import battleOfFrance from "../data/videos/battle-of-france-1940.json";
import battleOfBerlin from "../data/videos/battle-of-berlin-1945.json";
import operationBagration from "../data/videos/operation-bagration-1944.json";

export const videos: Video[] = [koreanWar, mongolEmpire, battleOfFrance, battleOfBerlin, operationBagration].map((v) => VideoSchema.parse(v));
