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
    docId: number
    text: string
    additionalProperties: any
}

export interface IndexDto {
    name: string
    models: string[]
    nTerms: number
    nDocs: number
    exampleDocuments: DocumentDto[]
}

export interface DocumentSearchResultDto {
    score?: number,
    document: DocumentDto
}

export interface QueryDto {
    query: string
    topK: number
    model: string
}
