from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chat.models import ChatSession, ChatMessage
from rag.retrieval import retrieve_chunks
from rag.prompts import SYSTEM_PROMPT
from chat.llm import generate_answer


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get("query")
        session_id = request.data.get("session_id")

        if not query:
            return Response({"error": "Query required"}, status=400)

        if session_id:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        else:
            session = ChatSession.objects.create(user=request.user)

        ChatMessage.objects.create(
            session=session,
            role="user",
            content=query,
        )

        retrieved = retrieve_chunks(request.user, query)

        if not retrieved:
            answer = "I could not find this information in your uploaded files."
            sources = []
        else:
            context = "\n\n".join(
                f"[{e.chunk.asset.original_name}] {e.chunk.content}"
                for e in retrieved
            )

            prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}
"""
            answer = generate_answer(prompt)
            seen = set()
            sources = []

            for e in retrieved:
                key = (e.chunk.asset.original_name, e.chunk.content[:200])
                if key in seen:
                    continue
                seen.add(key)

                sources.append({
                    "asset": e.chunk.asset.original_name,
                    "snippet": e.chunk.content[:200],
                })


        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=answer,
        )

        return Response(
            {
                "session_id": str(session.id),
                "answer": answer,
                "sources": sources,
            }
        )
