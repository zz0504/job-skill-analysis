import pandas as pd
from typing import Tuple, Optional, List
from app.core.logger import logger
from app.utils.parse_config import ParseConfig, ParseContext


class EncodingDetector:
    def __init__(self, config: Optional[ParseConfig] = None):
        self.config = config or ParseConfig()
        self.encoding_list = self.config.encoding_list
    
    def detect(self, file_path: str, context: ParseContext) -> Tuple[str, pd.DataFrame]:
        for encoding in self.encoding_list:
            try:
                logger.info(f"尝试使用 {encoding} 编码读取文件: {file_path}")
                
                df = pd.read_csv(
                    file_path, 
                    encoding=encoding, 
                    nrows=10,
                    dtype=str,
                    on_bad_lines='skip'
                )
                
                if df.empty:
                    logger.warning(f"{encoding} 编码解析结果为空")
                    context.log_encoding_attempt(encoding, False, "解析结果为空")
                    continue
                
                if len(df.columns) < 2:
                    logger.warning(f"{encoding} 编码解析列数不足")
                    context.log_encoding_attempt(encoding, False, "列数不足")
                    continue
                
                if self._contains_garbled(df):
                    logger.warning(f"{encoding} 编码解析包含乱码")
                    context.log_encoding_attempt(encoding, False, "包含乱码")
                    continue
                
                full_df = pd.read_csv(
                    file_path, 
                    encoding=encoding,
                    dtype=str,
                    on_bad_lines='skip'
                )
                
                logger.info(f"成功使用 {encoding} 编码读取文件，共 {len(full_df)} 行")
                context.log_encoding_attempt(encoding, True)
                context.detected_encoding = encoding
                
                return encoding, full_df
                
            except UnicodeDecodeError as e:
                logger.warning(f"{encoding} 编码解码失败: {str(e)}")
                context.log_encoding_attempt(encoding, False, f"UnicodeDecodeError: {str(e)}")
                continue
            except Exception as e:
                logger.warning(f"{encoding} 编码解析失败: {str(e)}")
                context.log_encoding_attempt(encoding, False, str(e))
                continue
        
        raise UnicodeDecodeError(
            'utf-8', 
            b'', 
            0, 
            1, 
            f'无法识别文件编码，已尝试: {", ".join(self.encoding_list)}'
        )
    
    def _contains_garbled(self, df: pd.DataFrame) -> bool:
        garbled_patterns = ['�', '鈥', '锟斤拷', '����', '锟�']
        
        for col in df.columns:
            for pattern in garbled_patterns:
                if pattern in str(col):
                    return True
        
        for col in df.columns:
            for val in df[col].head(5):
                for pattern in garbled_patterns:
                    if pattern in str(val):
                        return True
        
        return False


class SeparatorDetector:
    def __init__(self, config: Optional[ParseConfig] = None):
        self.config = config or ParseConfig()
        self.separator_list = self.config.separator_list
    
    def detect(self, file_path: str, encoding: str, context: ParseContext) -> str:
        with open(file_path, 'r', encoding=encoding) as f:
            lines = [f.readline() for _ in range(10)]
        
        sample_text = ''.join([line for line in lines if line.strip()])
        
        separator_scores = {}
        
        for sep in self.separator_list:
            counts = [line.count(sep) for line in lines if line.strip()]
            
            if not counts:
                continue
            
            avg_count = sum(counts) / len(counts)
            variance = sum((c - avg_count) ** 2 for c in counts) / len(counts)
            
            if avg_count > 0 and variance < avg_count:
                separator_scores[sep] = avg_count / (1 + variance)
        
        if not separator_scores:
            logger.warning("无法自动检测分隔符，使用默认逗号")
            context.log_separator_attempt(',', True, "默认分隔符")
            return ','
        
        best_sep = max(separator_scores, key=separator_scores.get)
        logger.info(f"检测到分隔符: {repr(best_sep)}, 得分: {separator_scores[best_sep]:.2f}")
        context.log_separator_attempt(best_sep, True, f"得分: {separator_scores[best_sep]:.2f}")
        context.detected_separator = best_sep
        
        return best_sep
