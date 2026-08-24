import { EmptyState } from "../../components/ui/EmptyState";
import { PageHeader } from "../../components/ui/PageHeader";

export default function DocumentsPage() {
  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto w-full max-w-7xl p-5 md:p-8">
        <PageHeader
          title="Documents"
          description="Manage knowledge documents used by the tourism intelligence platform."
        />

        <div className="mt-6">
          <EmptyState
            title="No documents available"
            description="Knowledge documents will appear here when the document management service is connected."
          />
        </div>
      </div>
    </main>
  );
}
