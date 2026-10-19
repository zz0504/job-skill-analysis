from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel


class ValidationLevel(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ErrorType(str, Enum):
    E001 = "E001"
    E002 = "E002"
    E003 = "E003"
    E004 = "E004"
    E005 = "E005"
    E006 = "E006"
    E999 = "E999"


class ValidationMessage(BaseModel):
    level: ValidationLevel
    message: str
    field: Optional[str] = None
    suggestion: Optional[str] = None


class ValidationResult(BaseModel):
    is_valid: bool
    messages: List[ValidationMessage] = []
    
    @property
    def errors(self) -> List[ValidationMessage]:
        return [m for m in self.messages if m.level == ValidationLevel.ERROR]
    
    @property
    def warnings(self) -> List[ValidationMessage]:
        return [m for m in self.messages if m.level == ValidationLevel.WARNING]


class DiagnosticInfo(BaseModel):
    error_type: ErrorType
    error_code: str
    error_message: str
    error_detail: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    suggestion: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ParseContext:
    def __init__(self, file_path: str, file_name: str, file_ext: str, batch_id: str):
        self.file_path = file_path
        self.file_name = file_name
        self.file_ext = file_ext
        self.batch_id = batch_id
        self.detected_encoding: Optional[str] = None
        self.detected_separator: Optional[str] = None
        self.attempt_count = 0
        self.encoding_attempts: List[Dict[str, Any]] = []
        self.separator_attempts: List[Dict[str, Any]] = []
        self.field_mappings: List[Dict[str, str]] = []
    
    def log_encoding_attempt(self, encoding: str, success: bool, error: Optional[str] = None):
        self.encoding_attempts.append({
            "encoding": encoding,
            "success": success,
            "error": error
        })
        self.attempt_count += 1
    
    def log_separator_attempt(self, separator: str, success: bool, reason: Optional[str] = None):
        self.separator_attempts.append({
            "separator": repr(separator),
            "success": success,
            "reason": reason
        })
    
    def log_field_mapping(self, source: str, target: str):
        self.field_mappings.append({
            "source": source,
            "target": target
        })


class ParseConfig(BaseModel):
    encoding_list: List[str] = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'gb18030', 'big5']
    encoding_timeout: int = 5
    separator_list: List[str] = [',', ';', '\t', '|']
    auto_detect_separator: bool = True
    required_fields: List[str] = ['岗位名称']
    field_mapping: Dict[str, str] = {
        '公司名称': '公司',
        '发布日期': '发布时间',
        '技能要求': '技能描述',
        '岗位职责': '技能描述',
        '职位名称': '岗位名称',
        'job_title': '岗位名称',
        'company': '公司'
    }
    
    class Config:
        frozen = True
