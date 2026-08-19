import type { ReactNode } from "react";

type EmptyStateProps = {
  title: string;
  description?: string;
  action?: ReactNode;
};

export function EmptyState({
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="rounded-xl border border-dashed border-border bg-surface-muted px-6 py-10 text-center">
      <h2 className="text-base font-semibold text-text-primary">
        {title}
      </h2>

      {description ? (
        <p className="mx-auto mt-2 max-w-md text-sm text-text-secondary">
          {description}
        </p>
      ) : null}

      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}
