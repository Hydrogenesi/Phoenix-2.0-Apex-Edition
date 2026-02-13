"""
Hydrogenesi Engine - The Structural Guardian
=============================================

Implements structural preservation, lineage tracking, and identity maintenance.

Domain: Continuity, Lineage, Identity Preservation
Purpose: Preserves structure and maintains identity through transformation
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LineageNode:
    """A node in the transformation lineage tree."""
    
    pattern_id: str
    operator: str
    timestamp: datetime
    value: Any
    energy: float
    parent_ids: List[str] = field(default_factory=list)
    
    def __repr__(self):
        return f"Node({self.operator}: {self.value}, E={self.energy:.3f})"


@dataclass
class Identity:
    """The essential identity of a pattern - preserved across transformations."""
    
    origin_id: str
    origin_value: Any
    origin_timestamp: datetime
    essence_signature: str
    
    def __repr__(self):
        return f"Identity(origin={self.origin_value}, sig={self.essence_signature[:8]}...)"


class HydrogesiEngine:
    """
    The Hydrogenesi Engine - Structure and Memory
    
    Domain: Continuity, Lineage, Identity Preservation
    Purpose: Preserves structure and maintains identity through transformation
    """
    
    def __init__(self):
        self.lineage_graph: Dict[str, LineageNode] = {}
        self.identities: Dict[str, Identity] = {}
        self.pattern_counter = 0
    
    def _generate_id(self) -> str:
        """Generate unique pattern ID."""
        self.pattern_counter += 1
        return f"Ψ_{self.pattern_counter:04d}"
    
    def _compute_essence(self, value: Any) -> str:
        """Compute the essence signature of a value."""
        # Simple hash-based essence signature
        import hashlib
        value_str = str(value)
        return hashlib.sha256(value_str.encode()).hexdigest()
    
    def record_genesis(self, pattern: Any) -> tuple[str, Identity]:
        """
        Record the genesis of a new pattern.
        Creates initial lineage node and identity.
        """
        pattern_id = self._generate_id()
        timestamp = datetime.now()
        
        # Create lineage node
        node = LineageNode(
            pattern_id=pattern_id,
            operator='⊕',
            timestamp=timestamp,
            value=pattern.value if hasattr(pattern, 'value') else pattern,
            energy=pattern.energy if hasattr(pattern, 'energy') else 1.0,
            parent_ids=[]
        )
        self.lineage_graph[pattern_id] = node
        
        # Create identity
        identity = Identity(
            origin_id=pattern_id,
            origin_value=pattern.value if hasattr(pattern, 'value') else pattern,
            origin_timestamp=timestamp,
            essence_signature=self._compute_essence(pattern.value if hasattr(pattern, 'value') else pattern)
        )
        self.identities[pattern_id] = identity
        
        return pattern_id, identity
    
    def record_transformation(self, pattern: Any, operator: str, parent_id: str) -> str:
        """
        Record a transformation in the lineage graph.
        Maintains continuity with parent pattern.
        """
        pattern_id = self._generate_id()
        timestamp = datetime.now()
        
        # Create lineage node with parent link
        node = LineageNode(
            pattern_id=pattern_id,
            operator=operator,
            timestamp=timestamp,
            value=pattern.value if hasattr(pattern, 'value') else pattern,
            energy=pattern.energy if hasattr(pattern, 'energy') else 1.0,
            parent_ids=[parent_id]
        )
        self.lineage_graph[pattern_id] = node
        
        # Preserve identity from parent
        if parent_id in self.identities:
            self.identities[pattern_id] = self.identities[parent_id]
        
        return pattern_id
    
    def record_convergence(self, pattern: Any, operator: str, parent_ids: List[str]) -> str:
        """
        Record convergence of multiple patterns.
        Maintains lineage from all parents.
        """
        pattern_id = self._generate_id()
        timestamp = datetime.now()
        
        # Create lineage node with multiple parents
        node = LineageNode(
            pattern_id=pattern_id,
            operator=operator,
            timestamp=timestamp,
            value=pattern.value if hasattr(pattern, 'value') else pattern,
            energy=pattern.energy if hasattr(pattern, 'energy') else 1.0,
            parent_ids=parent_ids
        )
        self.lineage_graph[pattern_id] = node
        
        # Preserve identity from first parent
        if parent_ids and parent_ids[0] in self.identities:
            self.identities[pattern_id] = self.identities[parent_ids[0]]
        
        return pattern_id
    
    def get_lineage(self, pattern_id: str) -> List[LineageNode]:
        """
        Get the complete lineage path from origin to current pattern.
        """
        if pattern_id not in self.lineage_graph:
            return []
        
        lineage = []
        current_id = pattern_id
        visited = set()
        
        # Traverse backwards through parent links
        while current_id and current_id not in visited:
            visited.add(current_id)
            node = self.lineage_graph[current_id]
            lineage.insert(0, node)
            
            # Follow first parent
            if node.parent_ids:
                current_id = node.parent_ids[0]
            else:
                current_id = None
        
        return lineage
    
    def get_identity(self, pattern_id: str) -> Optional[Identity]:
        """Get the preserved identity of a pattern."""
        return self.identities.get(pattern_id)
    
    def verify_continuity(self, pattern_id: str) -> bool:
        """
        Verify that continuity is maintained from origin to current pattern.
        """
        lineage = self.get_lineage(pattern_id)
        if not lineage:
            return False
        
        # Check that lineage forms continuous chain
        for i in range(1, len(lineage)):
            parent_node = lineage[i - 1]
            current_node = lineage[i]
            if parent_node.pattern_id not in current_node.parent_ids:
                return False
        
        return True
    
    def get_lineage_summary(self, pattern_id: str) -> str:
        """Get a human-readable summary of pattern lineage."""
        lineage = self.get_lineage(pattern_id)
        identity = self.get_identity(pattern_id)
        
        summary = f"Lineage for {pattern_id}:\n"
        summary += f"  Origin: {identity.origin_value if identity else 'Unknown'}\n"
        summary += f"  Path: "
        summary += " → ".join([node.operator for node in lineage])
        summary += f"\n  Steps: {len(lineage)}\n"
        summary += f"  Continuity: {'✓' if self.verify_continuity(pattern_id) else '✗'}\n"
        
        return summary
