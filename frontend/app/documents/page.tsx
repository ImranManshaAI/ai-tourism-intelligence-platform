import { Button } from "../../components/ui/Button";
import { EmptyState } from "../../components/ui/EmptyState";
import { PageHeader } from "../../components/ui/PageHeader";

export default function DocumentsPage() {
  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto w-full max-w-7xl p-5 md:p-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <PageHeader
            title="Documents"
            description="Manage knowledge documents used by the tourism intelligence platform."
          />

          <Button disabled>Upload Document</Button>
        </div>

        <div className="mt-6">
          <EmptyState
            title="No documents available"
            description="Document upload and knowledge management will be connected in a future implementation step."
          />
        </div>
      </div>
    </main>
  );
}