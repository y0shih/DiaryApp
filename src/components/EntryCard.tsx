
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { format } from "date-fns";

interface EntryCardProps {
  id: string;
  title: string;
  content: string;
  date: Date;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}

export const EntryCard = ({ id, title, content, date, onEdit, onDelete }: EntryCardProps) => {
  return (
    <Card className="w-full p-6 mb-4 transition-all duration-300 hover:shadow-lg">
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 mb-4 line-clamp-3">{content}</p>
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-500">{format(date, 'yyyy-MM-dd')}</span>
        <div className="space-x-2">
          <Button
            onClick={() => onEdit(id)}
            variant="secondary"
            className="hover:bg-gray-100 transition-colors"
          >
            Edit
          </Button>
          <Button
            onClick={() => onDelete(id)}
            variant="destructive"
            className="hover:bg-red-600 transition-colors"
          >
            Delete
          </Button>
        </div>
      </div>
    </Card>
  );
};
