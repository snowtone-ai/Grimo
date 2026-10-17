// v002 changes only the head item; reuse the established attachment/sole lifecycle.
import {installShushuStandardAppearance as installBase} from './shushu-standard-appearance-v001.mjs';
const flowerUrl=new URL('../equipment/standard-v002/shushu-head-flower-v002.glb',import.meta.url).href;
export async function installShushuStandardAppearance(options) {
 const equipment=await installBase({...options,flowerUrl:options.flowerUrl??flowerUrl});
 equipment.scope='Two principal sakura, small central overlap and five leaves; rounded satin petals v002 Human PENDING. Existing hind sole pads Human PASS, unchanged. Phone UNKNOWN.';
 return equipment;
}
