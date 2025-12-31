import Image from "next/image";
import { cn } from "@/lib/utils";

interface BrandLogoProps {
  className?: string;
  size?: number;
}

export function BrandLogo({ className, size = 32 }: BrandLogoProps) {
  return (
    <div className={cn("relative flex items-center justify-center", className)} style={{ width: size, height: size }}>
      <Image
        src="/icon.svg"
        alt="Brand Logo"
        width={size}
        height={size}
        className="object-contain"
        priority
      />
    </div>
  );
}
