import { ArrowUpIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export const Demo = () => {
    return (
        <div>
            <div className="m-10 flex items-start gap-2.5">
                <div className="flex flex-col w-full max-w-[320px] leading-1.5 p-4 border-gray-200 bg-gray-100 rounded-e-xl rounded-es-xl dark:bg-gray-700"> 
                    <p className="text-sm font-normal py-2.5 text-gray-900 dark:text-white">That's awesome. I think our users will really appreciate the improvements.</p>
                </div>
            </div>
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
        </div>
    );
};
