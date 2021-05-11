export const HITTypeParamOptions = [
    { name: "Reward", attrs: { type: "number", min: 0, step: 0.01 } },
    { name: "Title" },
    { name: "Description" },
    { name: "Keywords" },
    { name: "AutoApprovalDelayInSeconds", attrs: { type: "number", min: 0, step: 10 } },
    { name: "AssignmentDurationInSeconds", attrs: { type: "number", min: 0, step: 10 } },
];

export const defaultHITTypeParams = {
    "Reward": "0.01",
    "Title": "",
    "Description": "",
    "Keywords": "",
    "AutoApprovalDelayInSeconds": 600,
    "AssignmentDurationInSeconds": 1800,
    "QualificationRequirements": []
};

export const qualRequirementOptions = {
    "Comparator": [
            "LessThan",
            "LessThanOrEqualTo",
            "GreaterThan",
            "GreaterThanOrEqualTo",
            "EqualTo",
            "NotEqualTo",
            "Exists",
            "DoesNotExist",
            "In",
            "NotIn"
        ],
    "ActionsGuarded": [
            "Accept",
            "PreviewAndAccept",
            "DiscoverPreviewAndAccept"
        ]
};

export const defaultQualRequirements = {
    "QualificationTypeId": "",
    "Comparator": "",
    "IntegerValues": [],
    //"LocaleValues": [],   // intentionally excluded from default value
    "ActionsGuarded": ""
};

export const knownQualIds = [
    { id: "2ARFPLSP75KLA8M8DH1HTEQVJT3SY6", name: "Masters (Sandbox)" },
    { id: "2F1QJWKUDD8XADTFD2Q0G6UTO95ALH", name: "Masters (Production)" },
    { id: "00000000000000000040", name: "Worker_NumberHITsApproved" },
    { id: "00000000000000000071", name: "Worker_Locale" },
    { id: "00000000000000000060", name: "Worker_Adult" },
    { id: "000000000000000000L0", name: "Worker_PercentAssignmentsApproved" }
];

export const defaultHITParams = {
    "MaxAssignments": 1,
    "LifetimeInSeconds": 3600,
    "RequesterAnnotation": ""
};

export const defaultNumCreateHITs = 1;
