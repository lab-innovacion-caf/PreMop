import { FileUploader } from "@/components/file-uploader"
import { Header } from "@/components/header"

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto py-8">
        <div className="mx-auto max-w-2xl">
          <FileUploader />
        </div>
      </div>
    </main>
  )
}
