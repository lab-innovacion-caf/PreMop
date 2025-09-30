"use client"

import { ModeToggle } from "./mode-toggle"
import Image from "next/image"
import { Card, CardHeader } from "@/components/ui/card"
import logo from "@/assets/CAF-logo.png"

export function Header() {
  return (
    <Card className="border-b">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Image
              src={logo} 
              alt="CAF Logo"
              width={100}
              height={30}
              priority
              layout="fixed"
            />
          </div>
          <ModeToggle />
        </div>
      </CardHeader>
    </Card>
  )
} 