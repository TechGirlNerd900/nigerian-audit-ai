from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from enum import Enum

class DocumentType(str, Enum):
    FINANCIAL_STATEMENT = "financial_statement"
    TRIAL_BALANCE = "trial_balance"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    BANK_STATEMENT = "bank_statement"
    CONTRACT = "contract"
    AUDIT_REPORT = "audit_report"
    MANAGEMENT_LETTER = "management_letter"
    TAX_RETURN = "tax_return"
    PURCHASE_ORDER = "purchase_order"
    PAYMENT_VOUCHER = "payment_voucher"
    GENERAL_DOCUMENT = "general_document"

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL_SUCCESS = "partial_success"

class ExtractionMethod(str, Enum):
    OCR = "ocr"
    PDF_PARSING = "pdf_parsing"
    EXCEL_PARSING = "excel_parsing"
    TABLE_DETECTION = "table_detection"
    PATTERN_MATCHING = "pattern_matching"
    ML_EXTRACTION = "ml_extraction"

class ConfidenceLevel(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class ExtractedField(BaseModel):
    field_name: str = Field(..., description="Name of extracted field")
    value: Union[str, float, int, bool, None] = Field(..., description="Extracted value")
    confidence: float = Field(..., ge=0, le=100, description="Confidence in extraction (0-100)")
    extraction_method: ExtractionMethod
    source_location: Optional[Dict[str, Any]] = Field(None, description="Location in source document")
    validation_status: Optional[str] = Field(None, description="Validation status")
    alternative_values: Optional[List[str]] = Field(None, description="Alternative extracted values")

class ExtractedTable(BaseModel):
    table_name: Optional[str] = Field(None, description="Name or title of table")
    headers: List[str] = Field(..., description="Table column headers")
    rows: List[List[Union[str, float, int, None]]] = Field(..., description="Table data rows")
    confidence: float = Field(..., ge=0, le=100, description="Confidence in table extraction")
    source_location: Optional[Dict[str, Any]] = Field(None, description="Location in source document")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional table metadata")

class ExtractedFinancialData(BaseModel):
    document_type: DocumentType
    currency: Optional[str] = Field(None, description="Currency of amounts")
    amounts: Dict[str, float] = Field({}, description="Extracted monetary amounts")
    dates: Dict[str, str] = Field({}, description="Extracted dates")
    parties: Dict[str, str] = Field({}, description="Extracted party information")
    line_items: List[Dict[str, Any]] = Field([], description="Extracted line items")
    totals: Dict[str, float] = Field({}, description="Extracted total amounts")
    references: Dict[str, str] = Field({}, description="Reference numbers and IDs")

class DocumentMetadata(BaseModel):
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type of document")
    page_count: Optional[int] = Field(None, description="Number of pages")
    creation_date: Optional[str] = Field(None, description="Document creation date")
    modification_date: Optional[str] = Field(None, description="Last modification date")
    author: Optional[str] = Field(None, description="Document author")
    title: Optional[str] = Field(None, description="Document title")
    subject: Optional[str] = Field(None, description="Document subject")
    language: Optional[str] = Field(None, description="Document language")

class ProcessingOptions(BaseModel):
    extract_text: bool = Field(True, description="Extract text content")
    extract_tables: bool = Field(True, description="Extract tables")
    extract_images: bool = Field(False, description="Extract images")
    perform_ocr: bool = Field(True, description="Perform OCR on images")
    detect_signatures: bool = Field(False, description="Detect signatures")
    extract_financial_data: bool = Field(True, description="Extract financial data")
    validate_extracted_data: bool = Field(True, description="Validate extracted data")
    nigerian_formatting: bool = Field(True, description="Use Nigerian formatting rules")
    confidence_threshold: float = Field(70.0, ge=0, le=100, description="Minimum confidence threshold")

class ValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Overall validation result")
    validation_score: float = Field(..., ge=0, le=100, description="Validation score")
    issues: List[str] = Field([], description="Validation issues found")
    warnings: List[str] = Field([], description="Validation warnings")
    suggestions: List[str] = Field([], description="Improvement suggestions")

class ExtractionSummary(BaseModel):
    total_fields_extracted: int = Field(..., description="Total number of fields extracted")
    high_confidence_fields: int = Field(..., description="Fields with high confidence")
    tables_extracted: int = Field(..., description="Number of tables extracted")
    text_blocks_extracted: int = Field(..., description="Number of text blocks extracted")
    average_confidence: float = Field(..., ge=0, le=100, description="Average confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")

class ExtractedData(BaseModel):
    document_type: DocumentType
    extraction_summary: ExtractionSummary
    extracted_fields: List[ExtractedField] = Field([], description="Extracted fields")
    extracted_tables: List[ExtractedTable] = Field([], description="Extracted tables")
    financial_data: Optional[ExtractedFinancialData] = Field(None, description="Extracted financial data")
    full_text: Optional[str] = Field(None, description="Full extracted text")
    validation_result: Optional[ValidationResult] = Field(None, description="Validation results")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional extraction metadata")

class DocumentProcessingRequest(BaseModel):
    document_type: Optional[DocumentType] = Field(None, description="Expected document type")
    processing_options: Optional[ProcessingOptions] = Field(None, description="Processing options")
    custom_fields: Optional[List[str]] = Field(None, description="Custom fields to extract")
    validation_rules: Optional[List[str]] = Field(None, description="Custom validation rules")
    
    class Config:
        use_enum_values = True

class DocumentProcessingResult(BaseModel):
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    status: ProcessingStatus
    document_metadata: DocumentMetadata
    extracted_data: ExtractedData
    processing_log: List[str] = Field([], description="Processing log entries")
    error_messages: List[str] = Field([], description="Error messages if any")
    warnings: List[str] = Field([], description="Warning messages")

class DocumentProcessingResponse(BaseModel):
    success: bool = Field(True, description="Whether processing was successful")
    data: Optional[DocumentProcessingResult] = Field(None, description="Processing results")
    error: Optional[str] = Field(None, description="Error message if processing failed")
    timestamp: Optional[str] = Field(None, description="Processing timestamp")

class BatchDocumentProcessingRequest(BaseModel):
    documents: List[DocumentProcessingRequest] = Field(..., description="Documents to process")
    batch_options: Optional[Dict[str, Any]] = Field(None, description="Batch processing options")
    parallel_processing: bool = Field(True, description="Process documents in parallel")
    fail_fast: bool = Field(False, description="Stop on first error")
    
    @validator('documents')
    def validate_documents(cls, v):
        if not v:
            raise ValueError('At least one document must be provided')
        if len(v) > 100:
            raise ValueError('Maximum 100 documents allowed per batch')
        return v

class BatchDocumentProcessingResponse(BaseModel):
    success: bool = Field(True, description="Whether batch processing was successful")
    total_documents: int = Field(..., description="Total documents processed")
    successful_documents: int = Field(..., description="Successfully processed documents")
    failed_documents: int = Field(..., description="Failed document processing")
    results: List[DocumentProcessingResult] = Field([], description="Individual processing results")
    batch_summary: Optional[Dict[str, Any]] = Field(None, description="Batch processing summary")
    timestamp: Optional[str] = Field(None, description="Batch processing timestamp")

class TrialBalanceExtraction(BaseModel):
    accounts: Dict[str, float] = Field(..., description="Chart of accounts with balances")
    totals: Dict[str, float] = Field({}, description="Trial balance totals")
    currency: str = Field("NGN", description="Currency of amounts")
    period: Optional[str] = Field(None, description="Financial period")
    company_name: Optional[str] = Field(None, description="Company name")
    extraction_confidence: float = Field(..., ge=0, le=100, description="Extraction confidence")
    validation_status: str = Field(..., description="Validation status")

class FinancialStatementExtraction(BaseModel):
    statement_type: str = Field(..., description="Type of financial statement")
    line_items: Dict[str, float] = Field({}, description="Statement line items")
    subtotals: Dict[str, float] = Field({}, description="Statement subtotals")
    totals: Dict[str, float] = Field({}, description="Statement totals")
    notes: List[str] = Field([], description="Extracted notes")
    period: Optional[str] = Field(None, description="Statement period")
    comparative_figures: Optional[Dict[str, float]] = Field(None, description="Prior period figures")

class InvoiceExtraction(BaseModel):
    invoice_number: Optional[str] = Field(None, description="Invoice number")
    date: Optional[str] = Field(None, description="Invoice date")
    due_date: Optional[str] = Field(None, description="Due date")
    vendor_info: Dict[str, str] = Field({}, description="Vendor information")
    customer_info: Dict[str, str] = Field({}, description="Customer information")
    line_items: List[Dict[str, Any]] = Field([], description="Invoice line items")
    amounts: Dict[str, float] = Field({}, description="Invoice amounts")
    tax_info: Dict[str, float] = Field({}, description="Tax information")
    payment_terms: Optional[str] = Field(None, description="Payment terms")

class ReceiptExtraction(BaseModel):
    receipt_number: Optional[str] = Field(None, description="Receipt number")
    date: Optional[str] = Field(None, description="Receipt date")
    merchant_info: Dict[str, str] = Field({}, description="Merchant information")
    items: List[Dict[str, Any]] = Field([], description="Receipt items")
    amounts: Dict[str, float] = Field({}, description="Receipt amounts")
    payment_method: Optional[str] = Field(None, description="Payment method")
    tax_info: Dict[str, float] = Field({}, description="Tax information")

class BankStatementExtraction(BaseModel):
    account_info: Dict[str, str] = Field({}, description="Account information")
    statement_period: Optional[str] = Field(None, description="Statement period")
    opening_balance: Optional[float] = Field(None, description="Opening balance")
    closing_balance: Optional[float] = Field(None, description="Closing balance")
    transactions: List[Dict[str, Any]] = Field([], description="Bank transactions")
    summary: Dict[str, float] = Field({}, description="Statement summary")

class ContractExtraction(BaseModel):
    contract_number: Optional[str] = Field(None, description="Contract number")
    parties: List[str] = Field([], description="Contract parties")
    effective_date: Optional[str] = Field(None, description="Effective date")
    expiry_date: Optional[str] = Field(None, description="Expiry date")
    contract_value: Optional[float] = Field(None, description="Contract value")
    key_terms: List[str] = Field([], description="Key contract terms")
    payment_terms: Optional[str] = Field(None, description="Payment terms")

class OCRResult(BaseModel):
    extracted_text: str = Field(..., description="Extracted text content")
    confidence: float = Field(..., ge=0, le=100, description="OCR confidence score")
    language: str = Field("en", description="Detected language")
    word_count: int = Field(..., description="Number of words extracted")
    processing_time: float = Field(..., description="OCR processing time")
    character_accuracy: Optional[float] = Field(None, description="Character-level accuracy")

class DocumentClassificationResult(BaseModel):
    predicted_type: DocumentType
    confidence: float = Field(..., ge=0, le=100, description="Classification confidence")
    alternative_types: List[Dict[str, Any]] = Field([], description="Alternative document types")
    classification_features: List[str] = Field([], description="Features used for classification")

class DocumentQualityAssessment(BaseModel):
    overall_quality: str = Field(..., description="Overall document quality")
    readability_score: float = Field(..., ge=0, le=100, description="Text readability score")
    image_quality: Optional[float] = Field(None, ge=0, le=100, description="Image quality score")
    completeness_score: float = Field(..., ge=0, le=100, description="Document completeness")
    issues: List[str] = Field([], description="Quality issues identified")
    recommendations: List[str] = Field([], description="Quality improvement recommendations")

class DocumentProcessingError(BaseModel):
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Detailed error message")
    error_code: Optional[str] = Field(None, description="Error code")
    stage: str = Field(..., description="Processing stage where error occurred")
    recoverable: bool = Field(..., description="Whether error is recoverable")
    suggestions: List[str] = Field([], description="Error resolution suggestions")