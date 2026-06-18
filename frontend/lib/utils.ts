import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  // TODO: Keep or replace with shadcn/ui generated helper during UI setup.
  return twMerge(clsx(inputs));
}

