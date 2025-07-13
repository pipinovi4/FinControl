// ✅ Input.tsx
import * as React from "react";
import { cn } from "@/lib/utils";

type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, type = "text", ...props }, ref) => {
    return (
        <input
            type={type}
            className={cn(
                "flex w-full rounded-xl border border-input bg-white px-4 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1",
                className
            )}
            ref={ref}
            {...props}
        />
    );
});
Input.displayName = "Input";
export { Input };