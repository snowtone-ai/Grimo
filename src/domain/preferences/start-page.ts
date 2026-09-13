export const START_PAGE_STORAGE_KEY = "grimo.startPage";
export type StartPage = "tasks" | "grimo";
export const DEFAULT_START_PAGE: StartPage = "tasks";

const START_PAGE_CHANGE_EVENT = "grimo:start-page-change";

type ReadableStorage = Pick<Storage, "getItem">;
type WritableStorage = Pick<Storage, "setItem">;

export function isStartPage(value: unknown): value is StartPage {
  return value === "tasks" || value === "grimo";
}

export function readStartPage(storage?: ReadableStorage): StartPage {
  const target =
    storage ?? (typeof window !== "undefined" ? window.localStorage : null);

  if (!target) return DEFAULT_START_PAGE;

  const value = target.getItem(START_PAGE_STORAGE_KEY);
  return isStartPage(value) ? value : DEFAULT_START_PAGE;
}

export function writeStartPage(
  value: StartPage,
  storage?: WritableStorage,
): void {
  const target =
    storage ?? (typeof window !== "undefined" ? window.localStorage : null);

  if (!target) return;

  target.setItem(START_PAGE_STORAGE_KEY, value);

  // The native `storage` event only fires in other documents. Emit a small
  // same-document event so useSyncExternalStore subscribers update immediately.
  if (typeof window !== "undefined" && target === window.localStorage) {
    window.dispatchEvent(new Event(START_PAGE_CHANGE_EVENT));
  }
}

export function getStartPageSnapshot(): StartPage {
  return readStartPage();
}

export function getStartPageServerSnapshot(): StartPage {
  return DEFAULT_START_PAGE;
}

export function subscribeStartPage(onStoreChange: () => void): () => void {
  if (typeof window === "undefined") return () => {};

  const handleStorage = (event: StorageEvent) => {
    if (event.key === null || event.key === START_PAGE_STORAGE_KEY) {
      onStoreChange();
    }
  };
  const handleLocalChange = () => onStoreChange();

  window.addEventListener("storage", handleStorage);
  window.addEventListener(START_PAGE_CHANGE_EVENT, handleLocalChange);

  return () => {
    window.removeEventListener("storage", handleStorage);
    window.removeEventListener(START_PAGE_CHANGE_EVENT, handleLocalChange);
  };
}
