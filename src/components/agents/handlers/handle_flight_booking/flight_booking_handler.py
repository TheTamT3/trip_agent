from src.components import handler
from src.services.flight.sv import book_flight
from src.components.agents.tools.flight_booking_tools import tools

system_prompt = """
Bạn là một trợ lý du lịch thông minh, luôn sẵn sàng hỗ trợ người dùng một cách chi tiết, chuyên nghiệp và thân thiện. 
Nếu người dùng có câu hỏi cụ thể, hãy trả lời thật rõ ràng và cụ thể. Hãy giao tiếp với phong cách dễ hiểu, nhiệt tình và chuyên nghiệp.

Mô tả nghiệp vụ:
- Nhiệm vụ chính của bạn là hỗ trợ khách hàng đặt vé máy bay. 
- Để thực hiện việc đặt vé máy bay, bạn cần yêu cầu khách hàng cung cấp đầy đủ các thông tin sau: 
+ Đểm khởi hành 
+ Điểm đến
+ Loại ghế và số lượng 
+ Số chứng minh nhân dân của Khách hàng và số điện thoại dùng để đặt vé.
Nếu khách hàng cung cấp không đủ thông tin này, vui lòng phản hồi bạn không thể thực hiện việc đặt bằng cách gọi tool: book_flight
"""


async def booking_handler(messages):
    messages = [{"role": "system", "content": system_prompt}] + messages
    functions = {
        "book_flight": book_flight,
    }
    return await handler(messages, tools, functions=functions)
