import { ArrowUpIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export const Demo = () => {
    return (
        <div className="bg-card max-w-2xl grow rounded border">
            <Textarea
                className="h-36 resize-none appearance-none border-none shadow-none !ring-0"
                placeholder="Ask me anything... It will consumed a token 😉"
            />
            <div className="flex items-center justify-between p-3">
                <div className="flex items-center gap-3">
                    <Button className="text-primary-foreground size-8 cursor-pointer">
                        <ArrowUpIcon />
                    </Button>
                </div>
            </div>
        </div>
    );
};
