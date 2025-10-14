from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery

from containers import Container
from logger.logger import logger
from services.menu_service import SupplyPlanningMenuService
from utils.const import CallbackName
from utils.user_access import check_user_access


class SupplyPlanningHandler:
    def __init__(self, dp: Dispatcher):
        @dp.callback_query(F.data == CallbackName.SUPPLY_PLANNING_CALLBACK)
        async def handle_supply_planning_command(
            callback: CallbackQuery,
            bot: Bot,
            supply_planning_service: SupplyPlanningMenuService = Container.supply_planning_service(),
        ) -> None:
            # TODO вынести возможно в middleware
            user = callback.from_user.username
            if not await check_user_access(user):
                await callback.answer("❌ У вас нет доступа к этому разделу", show_alert=True)
                return
            msg = await callback.message.answer("📊 Начинаю формирование отчета...")

            try:
                planned_supplies = await supply_planning_service()

                if not planned_supplies:
                    await callback.message.answer("📭 Нет данных по поставкам")
                    return

                await callback.message.answer_document(planned_supplies, caption="📊 Отчет по планированию поставок")

            except Exception as e:
                logger.exception(f"Ошибка при обработке данных: {e}")
                await callback.message.answer("⚠️ Произошла ошибка при обработке данных")

            finally:
                await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
