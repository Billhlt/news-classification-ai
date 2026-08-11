export declare function chatWithAI(message: string, userId: string): Promise<string>;

export declare function saveNews(newsList: Array<[number, string]>): Promise<{
  success: boolean;
  saved_count: number;
  total_count: number;
  message: string;
  errors?: string[] | null;
}>;
