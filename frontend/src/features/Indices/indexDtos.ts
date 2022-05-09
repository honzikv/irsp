import { v4 as UUID } from 'uuid';

export interface PreprocessorConfigDto {
    lowercase: boolean
    removeAccentsBeforeStemming: boolean
    removePunctuation: boolean
    removeStopwords: boolean
    useStemmer: boolean
    lang: string
    removeAccentsAfterStemming: boolean
}

export interface IndexConfigDto {
    name: string
    preprocessorConfig: PreprocessorConfigDto
}

export interface DocumentDto {
    docId: string
    text: string
    additionalProperties: any
    score?: number
}

export interface IndexDto {
    name: string
    models: string[]
    nTerms: number
    nDocs: number
    exampleDocuments: DocumentDto[]
}

export interface DocumentSearchResultDto {
    documents: DocumentDto[]
    stopwords?: string[]
}

export interface QueryDto {
    query: string
    topK: number
    model: string
}
