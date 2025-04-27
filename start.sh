# 2) Start Voilà
voila notebooks --no-browser --port 8866 &
VOILA_PID=$!


# 3) Start React dev server (assumes you run Vite)
cd prognosix-dashboard
npm install
npm run dev &
VITE_PID=$!

# 4) Wait until user hits Ctrl-C
trap "kill $VOILA_PID $VITE_PID" SIGINT
wait
