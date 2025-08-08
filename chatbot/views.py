import os
import json
import traceback

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, UploadedImage
from .rag_engine import run_chatbot, search_vector_db_image


@method_decorator(csrf_exempt, name="dispatch")
class ChatBotView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            query = body.get("query", "")
            history = body.get("history", [])

            print(f"📝 받은 쿼리: {query}")

            try:
                result = run_chatbot(query, history=history)
                return JsonResponse({"response": result})
            except Exception as rag_error:
                print(f"❌ RAG 엔진 오류: {rag_error}")
                traceback.print_exc()
                return JsonResponse({
                    "response": f"죄송합니다. AI 검색 기능에 문제가 있습니다. (오류: {str(rag_error)[:200]})"
                })

        except Exception as e:
            print(f"❌ 전체 오류: {str(e)}")
            traceback.print_exc()
            return JsonResponse({
                "error": f"서버 오류: {str(e)}"
            }, status=500)

@method_decorator(csrf_exempt, name="dispatch")
class ModelSearchView(View):
    def post(self, request):
        image_file = request.FILES.get("image")
        if not image_file:
            return HttpResponseBadRequest("No image file uploaded.")

        print(f"🖼️ 이미지 업로드됨: {image_file.name} ({image_file.size} bytes)")

        import tempfile
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"upload_{image_file.name}")
        
        print(f"💾 임시 저장 경로: {temp_path}")

        try:
            with open(temp_path, "wb+") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            
            print(f"✅ 파일 저장 완료: {os.path.exists(temp_path)}")

            print("🔍 이미지 검색 시작...")
            from .rag_engine import search_vector_db_image
            model_code = search_vector_db_image(temp_path)
            print(f"🔍 검색 결과: {model_code}")
            
            if model_code and model_code != -1:
                model_parts = str(model_code).split('_')
                
                response_data = {
                    "success": True,
                    "model_code": model_code,
                    "model_name": model_code,
                    "model": str(model_code),
                    "product_info": {
                        "type": "세탁기" if "세탁기" in str(model_code) else "세탁건조기",
                        "capacity": "21kg" if "21kg" in str(model_code) else "용량 확인 필요",
                        "model": model_parts[2] if len(model_parts) > 2 else "모델명 확인 필요",
                        "color": "이녹스" if "이녹스" in str(model_code) else "색상 확인 필요",
                    },
                    "message": "이미지에서 모델을 성공적으로 인식했습니다."
                }
            else:
                response_data = {
                    "success": False,
                    "model_code": -1,
                    "model_name": "인식 실패",
                    "model": "모델 정보를 찾을 수 없습니다.",
                    "product_info": {
                        "type": "알 수 없음",
                        "capacity": "알 수 없음", 
                        "model": "알 수 없음",
                        "color": "알 수 없음",
                    },
                    "message": "이미지에서 모델을 인식할 수 없습니다."
                }
            
            print(f"📤 응답 데이터: {response_data}")
            return JsonResponse(response_data)
        except Exception as e:
            print(f"❌ 이미지 검색 오류: {str(e)}")
            traceback.print_exc()
            
            return JsonResponse({
                "success": False,
                "model_code": -1,
                "model": "이미지 분석 중 오류가 발생했습니다.",
                "error": str(e)[:200]
            }, status=500)
        finally:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    print(f"🗑️ 임시 파일 삭제: {temp_path}")
            except Exception as cleanup_error:
                print(f"⚠️ 임시 파일 삭제 실패: {cleanup_error}")


@method_decorator(csrf_exempt, name="dispatch")
class ConversationView(View):
    """대화 관리 API"""
    
    def get(self, request):
        """사용자의 대화 목록 조회"""
        if not request.user.is_authenticated:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
        
        conversations = Conversation.objects.filter(user=request.user, is_active=True)
        conversation_list = []
        
        for conv in conversations:
            conversation_list.append({
                'id': conv.id,
                'title': conv.title,
                'created_at': conv.created_at.isoformat(),
                'updated_at': conv.updated_at.isoformat(),
                'message_count': conv.messages.count()
            })
        
        return JsonResponse({"conversations": conversation_list})
    
    def post(self, request):
        """새 대화 생성"""
        if not request.user.is_authenticated:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
        
        try:
            body = json.loads(request.body)
            title = body.get("title", "새 대화")
            
            conversation = Conversation.objects.create(
                user=request.user,
                title=title
            )
            
            return JsonResponse({
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat()
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class MessageView(View):
    """메시지 관리 API"""
    
    def get(self, request, conversation_id):
        """특정 대화의 메시지 조회"""
        if not request.user.is_authenticated:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
        
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        messages = conversation.messages.all()
        
        message_list = []
        for msg in messages:
            message_list.append({
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'created_at': msg.created_at.isoformat()
            })
        
        return JsonResponse({
            "conversation_id": conversation.id,
            "title": conversation.title,
            "messages": message_list
        })
    
    def post(self, request, conversation_id):
        """메시지 전송 및 챗봇 응답"""
        if not request.user.is_authenticated:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
        
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            body = json.loads(request.body)
            user_message = body.get("message", "")
            
            if not user_message:
                return JsonResponse({"error": "메시지가 비어있습니다."}, status=400)
            
            # 사용자 메시지 저장
            user_msg = Message.objects.create(
                conversation=conversation,
                role='user',
                content=user_message
            )
            
            # 대화 히스토리 가져오기
            history = []
            for msg in conversation.messages.all():
                history.append({
                    'role': msg.role,
                    'content': msg.content
                })
            
            # 챗봇 응답 생성
            chatbot_response = run_chatbot(user_message, history=history)
            
            # 챗봇 응답 저장
            assistant_msg = Message.objects.create(
                conversation=conversation,
                role='assistant',
                content=chatbot_response
            )
            
            # 대화 제목 업데이트 (첫 번째 메시지인 경우)
            if conversation.messages.count() == 2:  # 사용자 메시지 + 챗봇 응답
                conversation.title = user_message[:50] + "..." if len(user_message) > 50 else user_message
                conversation.save()
            
            return JsonResponse({
                "user_message": {
                    'id': user_msg.id,
                    'role': user_msg.role,
                    'content': user_msg.content,
                    'created_at': user_msg.created_at.isoformat()
                },
                "assistant_message": {
                    'id': assistant_msg.id,
                    'role': assistant_msg.role,
                    'content': assistant_msg.content,
                    'created_at': assistant_msg.created_at.isoformat()
                }
            })
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class ConversationDetailView(View):
    """대화 상세 관리 API"""
    
    def delete(self, request, conversation_id):
        """대화 삭제"""
        if not request.user.is_authenticated:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
        
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            conversation.is_active = False
            conversation.save()
            
            return JsonResponse({"message": "대화가 삭제되었습니다."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    def put(self, request, conversation_id):
        """대화 제목 수정"""
        if not request.user.is_authenticated:
            return JsonResponse({"error": "로그인이 필요합니다."}, status=401)
        
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            body = json.loads(request.body)
            title = body.get("title", "")
            
            if title:
                conversation.title = title
                conversation.save()
                
                return JsonResponse({
                    "id": conversation.id,
                    "title": conversation.title
                })
            else:
                return JsonResponse({"error": "제목이 비어있습니다."}, status=400)
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
