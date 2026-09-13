export const START_PAGE_STORAGE_KEY = "grimo.startPage";
export type StartPage = "tasks" | "grimo";
export const DEFAULT_START_PAGE: StartPage = "tasks";

export function isStartPage(value: unknown): value is StartPage {
  return value === "tasks" || value === "grimo";
}

export function readStartPage(storage: Pick<Storage, "getItem"> = localStorage): StartPage {
  const value = storage.getItem(START_PAGE_STORAGE_KEY);
  return isStartPage(value) ? value : DEFAULT_START_PAGE;
}

export function writeStartPage(value: StartPage, storage: Pick<Storage, "setItem"> = localStorage): void {
  storage.setItem(START_PAGE_STORAGE_KEY, value);
}
