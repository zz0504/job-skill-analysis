from typing import Optional
import pandas as pd
from fastapi import HTTPException
from app.utils.parse_config import ErrorType, DiagnosticInfo
from app.core.logger import logger


class ParseErrorHandler:
    @staticmethod
    def handle_parse_error(error: Exception, context: dict = None) -> HTTPException:
        error_mapping = {
            UnicodeDecodeError: {
                "error_type": ErrorType.E001,
                "error_code": "E001",
                "message": "文件编码识别失败",
                "suggestion": "请确保文件使用UTF-8或GBK编码保存"
            },
            pd.errors.ParserError: {
                "error_type": ErrorType.E002,
                "error_code": "E002",
                "message": "文件格式解析失败",
                "suggestion": "请检查CSV文件格式是否正确，各行列数是否一致"
            },
            pd.errors.EmptyDataError: {
                "error_type": ErrorType.E003,
                "error_code": "E003",
                "message": "文件内容为空",
                "suggestion": "请确保文件包含有效的数据内容"
            },
            KeyError: {
                "error_type": ErrorType.E004,
                "error_code": "E004",
                "message": "必需字段缺失",
                "suggestion": "请确保文件包含'岗位名称'列"
            },
            ValueError: {
                "error_type": ErrorType.E005,
                "error_code": "E005",
                "message": "数据格式错误",
                "suggestion": "请检查数据格式是否正确"
            },
            PermissionError: {
                "error_type": ErrorType.E006,
                "error_code": "E006",
                "message": "文件权限不足",
                "suggestion": "请检查文件读写权限"
            }
        }
        
        error_info = None
        for error_type, mapping in error_mapping.items():
            if isinstance(error, error_type):
                error_info = mapping
                break
        
        if not error_info:
            error_info = {
                "error_type": ErrorType.E999,
                "error_code": "E999",
                "message": "未知错误",
                "suggestion": "请联系管理员"
            }
        
        diagnostic = DiagnosticInfo(
            error_type=error_info["error_type"],
            error_code=error_info["error_code"],
            error_message=error_info["message"],
            error_detail=str(error),
            suggestion=error_info["suggestion"],
            context=context
        )
        
        logger.error(
            f"解析错误 [{diagnostic.error_code}]: {diagnostic.error_message}",
            exc_info=True
        )
        
        user_message = f"{diagnostic.error_message}"
        if diagnostic.suggestion:
            user_message += f"，{diagnostic.suggestion}"
        
        return HTTPException(
            status_code=400,
            detail=user_message
        )
    
    @staticmethod
    def handle_missing_fields(df_columns: list, required_fields: list) -> Optional[str]:
        missing = [field for field in required_fields if field not in df_columns]
        
        if missing:
            message = f"缺少必需字段: {', '.join(missing)}"
            logger.warning(message)
            return message
        
        return None
