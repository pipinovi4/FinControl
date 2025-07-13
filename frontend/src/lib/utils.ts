// lib/utils.ts
// Комбінує правдиві className-рядки (аналог clsx)
export function cn(...inputs: Array<string | false | null | undefined>): string {
    return inputs.filter(Boolean).join(' ');
}
