import type { SelectHTMLAttributes } from "react";

type SelectProps = SelectHTMLAttributes<HTMLSelectElement>;

export function Select({
  className = "",
  children,
  ...props
}: SelectProps) {
  return (
    <select
      className={`min-h-10 w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text-primary focus:border-accent focus:outline-none focus:ring-2 focus:ring-ring/20 disabled:cursor-not-allowed disabled:bg-surface-muted disabled:opacity-60 ${className}`}
      {...props}
    >
      {children}
    </select>
  );
}
