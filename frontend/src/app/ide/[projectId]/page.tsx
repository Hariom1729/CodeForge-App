import IDEWorkspace from "@/components/IDEWorkspace";

export default async function IDEPage({ params }: { params: Promise<{ projectId: string }> }) {
  const resolvedParams = await params;
  return <IDEWorkspace projectId={resolvedParams.projectId} />;
}
