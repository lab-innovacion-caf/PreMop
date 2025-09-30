"use client"
import { useState, useEffect, useRef } from "react"
import { useDropzone } from "react-dropzone"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Download, Upload } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { Toaster } from "@/components/ui/toaster"

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'
console.log('Backend URL:', BACKEND_URL)

export function FileUploader() {
  const [file, setFile] = useState<File | null>(null)
  const [processing, setProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [outputFile, setOutputFile] = useState<string | null>(null)
  const [websocketId, setWebsocketId] = useState<string | null>(null)
  const { toast } = useToast()
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    // Create WebSocket connection
    const ws = new WebSocket(`${BACKEND_URL.replace('http', 'ws')}/ws`)
    wsRef.current = ws

    ws.onopen = () => {
      console.log('Connected to WebSocket')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('Received message:', data)

        if (data.type === 'connection_established') {
          setWebsocketId(data.websocket_id)
        }
        else if (data.type === 'progress') {
          setProgress(data.value)
        }
      } catch (e) {
        console.error('Error parsing message:', e)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      console.log('Disconnected from WebSocket')
    }

    // Cleanup on unmount
    return () => {
      ws.close()
    }
  }, []) // Empty dependency array - only run once on mount

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0])
      setProgress(0)
      setOutputFile(null)
    }
  })

  const handleProcess = async () => {
    if (!file || !websocketId) return

    setProcessing(true)
    const formData = new FormData()
    formData.append('file', file)
    formData.append('websocket_id', websocketId)

    try {
      const response = await fetch(`${BACKEND_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Processing failed')

      const result = await response.json()
      setOutputFile(`${BACKEND_URL}${result.downloadUrl}`)
      toast({
        title: "Procesamiento completado",
        description: "El documento ha sido generado exitosamente.",
      })
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Hubo un error al procesar el archivo.",
      })
      setProgress(0)
    } finally {
      setProcessing(false)
    }
  }

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Subir Documento</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div
            {...getRootProps()}
            className="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:border-primary transition-colors"
          >
            <input {...getInputProps()} />
            <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
            <p className="mt-2 text-sm text-muted-foreground">
              Arrastre un archivo PDF aquí o haga clic para seleccionar
            </p>
          </div>

          {file && (
            <div className="space-y-4">
              <p className="text-sm">
                Archivo seleccionado: <span className="font-medium">{file.name}</span>
              </p>
              <Button
                onClick={handleProcess}
                disabled={processing}
                className="w-full"
              >
                {processing ? "Procesando..." : "Procesar archivo"}
              </Button>
            </div>
          )}

          {(processing || progress > 0) && (
            <div className="space-y-2">
              <Progress value={progress} className="w-full" />
              <p className="text-sm text-center text-muted-foreground">
                {progress.toFixed(0)}% completado
              </p>
            </div>
          )}

          {outputFile && (
            <Button
              variant="outline"
              className="w-full"
              onClick={() => window.open(outputFile, '_blank')}
            >
              <Download className="mr-2 h-4 w-4" />
              Descargar documento generado
            </Button>
          )}
        </CardContent>
      </Card>
      <Toaster />
    </>
  )
}